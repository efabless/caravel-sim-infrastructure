import cocotb
from cocotb.triggers import RisingEdge, NextTimeStep, Edge
from collections import namedtuple
from tabulate import tabulate
from cocotb.queue import Queue
import os
import json
from cocotb_coverage.coverage import CoverPoint

APB_Transaction = namedtuple("APB_Transaction", ["address", "write", "data"])
IRQ_Transaction = namedtuple("IRQ_Transaction", ["irq", "im_val"])


class EF_apbModel():
    def __init__(self, hdl, json_file, ip_name="apb_ip", cov_hierarchy="apb_ip", coverage_enabled=False, logging_enabled=False) -> None:
        if not (coverage_enabled or logging_enabled):
            return
        apb_queue = Queue()
        self.ip_regs = APB_regs(json_file=json_file)
        EF_apbMonitor(hdl, apb_queue, self.ip_regs)
        apbModel(apb_queue, self.ip_regs, ip_name, cov_hierarchy, coverage_enabled, logging_enabled)


class apbModel():
    def __init__(self, queue, ip_regs, ip_name, cov_hierarchy="apb_ip", coverage_enabled=False, logging_enabled=False) -> None:
        self.ip_regs = ip_regs
        self.ip_regs_dict = ip_regs.get_regs()
        self.coverge_enabled = coverage_enabled
        self.logging_enabled = logging_enabled
        if self.logging_enabled:
            self.configure_logger(logger_file=f"{ip_name}_apb.log")
        self._thread = cocotb.scheduler.add(self._model(queue))
        if self.coverge_enabled:
            self.apb_cov = EF_apbCoverage(cov_hierarchy, self.ip_regs_dict, ip_regs.get_irq_exist())

    async def _model(self, queue):
        while True:
            transaction = await self._get_transactions(queue)
            cocotb.log.debug(f"[{__class__.__name__}][_model] {transaction}")
            if self.logging_enabled:
                self.log_operation(transaction)
            if self.coverge_enabled:
                self.sample_coverage(transaction)

    def sample_coverage(self, transaction):
        if "APB_Transaction" in str(type(transaction)):
            self.apb_cov.apb_cov(transaction)
        elif "IRQ_Transaction" in str(type(transaction)):
            self.apb_cov.irq_cov(transaction)
       

    async def _get_transactions(self, queue):
        transaction = await queue.get()
        cocotb.log.debug(f"[{__class__.__name__}][_get_transactions] getting transaction {transaction} from monitor type {type(transaction)}")
        # write to reg model
        if "APB_Transaction" in str(type(transaction)):
            if transaction.write:
                self.ip_regs.write_reg_value(transaction.address, transaction.data)
        return transaction

    def configure_logger(self, logger_file="log.txt"):
        if not os.path.exists("loggers"):
            os.makedirs("loggers")
        self.logger_file = f"{os.getcwd()}/loggers/{logger_file}"
        # # log the header
        self.log_operation(None, header_logged=True)

    def log_operation(self, transaction, header_logged=False):
        if header_logged:
            # Log the header
            header = tabulate([], headers=["Time", "Type", "Address", "Data"], tablefmt="grid")
            with open(self.logger_file, 'w') as f:
                f.write(f"{header}\n")
        else:
            if "APB_Transaction" in str(type(transaction)):
                try:
                    register_name = self.ip_regs_dict[transaction.address & 0xffff]['name']
                except KeyError:
                    register_name = ""
                table_data = [(
                    f"{cocotb.utils.get_sim_time(units='ns')} ns",
                    "read" if transaction.write == 0 else "wrote",
                    f"{hex(transaction.address)}({register_name})",
                    transaction.data if "x" in transaction.data.binstr else hex(transaction.data.integer)
                )]
            elif "IRQ_Transaction" in str(type(transaction)):
                table_data = [(
                    f"{cocotb.utils.get_sim_time(units='ns')} ns",
                    "irq",
                    f"{hex(transaction.irq)}",
                    f"im = {hex(transaction.im_val)}"
                )]
            table = tabulate(table_data, tablefmt="grid")
            with open(self.logger_file, 'a') as f:
                f.write(f"{table}\n")


class APB_regs():
    def __init__(self, json_file) -> None:
        with open(json_file, 'r') as file:
            self.data = json.load(file)
        self.init_regs()
        cocotb.log.info(f"[{__class__.__name__}] {self.get_regs()}")

    def init_regs(self):
        regs = {}
        address = 0
        self.irq_exist = False
        for reg in self.data["regs"]:
            regs[address] = reg
            if "init" not in reg:
                regs[address]["val"] = 0
            else:
                regs[address]["val"] = int(reg["init"])
            address += 4
        if "flags" in self.data:
            size = len(self.data["flags"])
            reg_icr = {'name': 'icr', 'size': size, 'mode': 'fw', 'init': '0', 'fields': [{'name': 'icr', 'from': '0', 'size': size, 'port': ''}], "val": 0}
            reg_ris = {'name': 'ris', 'size': size, 'mode': 'fr', 'init': '0', 'fields': [{'name': 'ris', 'from': '0', 'size': size, 'port': ''}], "val": 0}
            reg_im = {'name': 'im', 'size': size, 'mode': 'rw', 'init': '0', 'fields': [{'name': 'im', 'from': '0', 'size': size, 'port': ''}], "val": 0}
            reg_mis = {'name': 'mis', 'size': size, 'mode': 'fr', 'init': '0', 'fields': [{'name': 'mis', 'from': '0', 'size': size, 'port': ''}], "val": 0}
            address = 0xf00
            regs[address] = reg_icr
            regs[address + 4] = reg_ris
            regs[address + 8] = reg_im
            regs[address + 12] = reg_mis
            self.irq_exist = True
        self.regs = regs

    def get_regs(self):
        return self.regs

    def get_irq_exist(self):
        return self.irq_exist

    def write_reg_value(self, address, value):
        address = address & 0xffff
        cocotb.log.debug(f"[{__class__.__name__}] value before write to address {hex(address)}: {hex(self.regs[address]['val'])}")
        if "w" in self.regs[address]["mode"]:
            self.regs[address]["val"] = value & ((1 << int(self.regs[address]["size"])) - 1)
        cocotb.log.info(f"[{__class__.__name__}] value after write to address {hex(address)}: {hex(self.regs[address]['val'])}")

    def read_reg_value(self, address):
        return self.regs[address]["val"]


class EF_apbMonitor:
    def __init__(self, hdl, queue, ip_regs) -> None:
        self.apb_hdl = hdl
        self.ip_regs_dict = ip_regs.get_regs()
        self._queue_fork = cocotb.scheduler.add(self.apb_monitor(queue))
        if ip_regs.get_irq_exist():
            self._irq_fork = cocotb.scheduler.add(self.irq_monitor(queue))
        cocotb.log.info("[TEST] Start UART APB Monitor")

    async def irq_monitor(self, queue):
        self.irq_hdls()
        while True:
            await Edge(self.irq_hdl)
            transaction = IRQ_Transaction(irq=self.irq_hdl.value.integer, im_val=self.ip_regs_dict[0xF08]["val"])
            cocotb.log.debug(f"[{__class__.__name__}][irq_monitor] sending transaction {transaction} to queue")
            queue.put_nowait(transaction)

    async def apb_monitor(self, queue):
        self.apb_hdls()
        while True:
            await RisingEdge(self.apb_clk_hdl)
            # check reset
            if self.apb_reset_hdl.value.integer == 0:
                continue
            # check enable and select
            if self.apb_en_hdl.value.integer != 1 or self.apb_select_hdl.value.integer != 1:
                continue
            # new transaction
            await cocotb.start(self._transaction_monitor(queue))
            await NextTimeStep()

    async def _transaction_monitor(self, queue):
        adress = self.apb_addr_hdl.value.integer
        write = self.apb_wen_hdl.value.integer
        if write:
            data = self.apb_wdata_hdl.value
            # wait for ack
            while True:
                await RisingEdge(self.apb_clk_hdl)
                await NextTimeStep()
                if self.apb_ack_hdl.value.integer == 1:
                    break
        else:
            # wait for ack
            while True:
                await RisingEdge(self.apb_clk_hdl)
                await NextTimeStep()
                if self.apb_ack_hdl.value.integer == 1:
                    break
            data = self.apb_rdata_hdl.value
        transaction = APB_Transaction(address=adress, write=write, data=data)
        cocotb.log.debug(f"[{__class__.__name__}][_apb_monitor_] sending transaction {transaction} to queue")
        queue.put_nowait(transaction)
        return

    def apb_hdls(self):
        self.apb_clk_hdl = self.apb_hdl.PCLK
        self.apb_reset_hdl = self.apb_hdl.PRESETn
        self.apb_addr_hdl = self.apb_hdl.PADDR
        self.apb_select_hdl = self.apb_hdl.PSEL
        self.apb_en_hdl = self.apb_hdl.PENABLE
        self.apb_wdata_hdl = self.apb_hdl.PWDATA
        self.apb_wen_hdl = self.apb_hdl.PWRITE
        self.apb_rdata_hdl = self.apb_hdl.PRDATA
        self.apb_ack_hdl = self.apb_hdl.PREADY

    def irq_hdls(self):
        self.irq_hdl = self.apb_hdl.irq

class EF_apbCoverage:
    def __init__(self, hierarchy, ip_regs_dict, irq_exist=False) -> None:
        self.hierarchy = hierarchy
        self.ip_regs_dict = ip_regs_dict
        # initialize coverage no covearge happened just sample nothing so the coverge is initialized
        self.apb_cov(None, do_sampling=False)
        if irq_exist:
            self.irq_cov(None, do_sampling=False)

    def apb_cov(self, operation, do_sampling=True):
        cov_points = self._cov_points()

        @self.apply_decorators(decorators=cov_points)
        def sample(operation):
            pass
        if do_sampling:
            sample(operation)

    def irq_cov(self, operation, do_sampling=True):
        im_size = int(self.ip_regs_dict[3848]["size"])

        @CoverPoint(
            f"{self.hierarchy}.irq.irq",
            xf=lambda operation: operation.irq,
            bins=[0 , 1],
            bins_labels=["clear", "set"],
        )
        @CoverPoint(
            f"{self.hierarchy}.irq.irq_im",
            xf=lambda operation: (operation.irq, operation.im_val),
            bins=[(i, 1 << j) for i in [0, 1] for j in range(im_size)],
            bins_labels=[f"({i}, flag{j})" for i in ["clear", "set"] for j in range(im_size)],
            rel=lambda val, b: val[1] == b[1] and val[0] == b[0]
        )
        def sample(operation):
            pass
        if do_sampling:
            sample(operation)

    def _cov_points(self):
        cov_points = []
        for reg_addr, reg in self.ip_regs_dict.items():
            cocotb.log.debug(f"register: {reg['name']} reg_addr: {reg_addr}")
            for field in reg["fields"]:
                for access in ["write", "read"]:
                    # skip non write or read fields
                    if access == "write" and "w" not in reg["mode"]:
                        continue
                    if access == "read" and "r" not in reg["mode"]:
                        continue
                    field_size = int(field["size"])
                    field_start = int(field["from"])
                    if field_size < 5:
                        cov_points.append(CoverPoint(
                            f"{self.hierarchy}.regs.{reg['name']}.{field['name']}.{access}",
                            xf=lambda operation, field_start=field_start, field_size=field_size: (operation.address & 0xffff, "write" if operation.write else "read", 0x0 if "x" in operation.data.binstr else (operation.data.integer >> field_start) &  (1 << field_size) - 1),
                            bins=[i for i in range(2**field_size)],
                            bins_labels=[format(i, f'0{field_size}b') for i in range(2 ** field_size)],
                            rel=lambda val, b, address=reg_addr, access=access: val[1] == access and val[0] == address and val[2] == b
                            # rel=lambda val, b:  address
                        ))
                    else:
                        cov_points.append(CoverPoint(
                            f"{self.hierarchy}.regs.{reg['name']}.{field['name']}.{access}",
                            xf=lambda operation, field_start=field_start, field_size=field_size: (operation.address & 0xffff, "write" if operation.write else "read", 0x0 if "x" in operation.data.binstr else (operation.data.integer >> field_start) &  (1 << field_size) - 1),
                            bins=[(1 << i, (1 << i + 1) - 1) if i != 0 else (0, 1) for i in range(field_size)],
                            bins_labels=[f"from {hex(1 << i)} to {hex((1 << i + 1) - 1)}" if i != 0 else f"from {hex(0)} to {hex(1)}" for i in range(field_size)],
                            rel=lambda val, b, address=reg_addr, access=access: val[1] == access and val[0] == address and b[0] <= val[2] <= b[1]
                        ))
        return cov_points

    def apply_decorators(self, decorators):
        def decorator_wrapper(func):
            for decorator in decorators:
                func = decorator(func)
            return func
        return decorator_wrapper

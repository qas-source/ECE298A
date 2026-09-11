import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")
    
    # 1. Initialize inputs
    dut.ena.value = 1       # Enable the design
    dut.ui_in.value = 0     # Clear data input
    dut.uio_in.value = 0    # Set uio_in[0] (load enable) to 0
    
    # 2. Start a 10us clock
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # 3. Reset the design
    dut._log.info("Reset")
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 2)
    
    # 4. Test normal counting
    dut._log.info("Test normal counting")
    dut.uio_in.value = 0    # Ensure load is low
    await ClockCycles(dut.clk, 5) # Let it count for 5 cycles
    assert dut.uo_out.value == 5, f"Expected 5, got {dut.uo_out.value}"
    
    # 5. Test the load function
    dut._log.info("Test loading a value (50)")
    dut.ui_in.value = 50    # The value to load
    dut.uio_in.value = 1    # Set uio_in[0] HIGH to trigger load
    await ClockCycles(dut.clk, 1) # Wait one clock cycle for the load to register
    assert dut.uo_out.value == 50, f"Expected 50, got {dut.uo_out.value}"
    
    # 6. Test counting up from the loaded value
    dut._log.info("Test counting from loaded value")
    dut.uio_in.value = 0    # Set uio_in[0] LOW to resume counting
    await ClockCycles(dut.clk, 2) # Count for 2 cycles
    assert dut.uo_out.value == 52, f"Expected 52, got {dut.uo_out.value}"
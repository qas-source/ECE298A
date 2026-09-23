import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")
    
    # 1. Initialize inputs
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0 # oe=0, load=0
    
    # 2. Start a 10us clock
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # 3. Reset the design
    dut._log.info("Reset")
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    
    # Align to the falling edge before releasing reset to avoid race conditions
    await FallingEdge(dut.clk)
    dut.rst_n.value = 1
    
    # 4. Test normal counting
    dut._log.info("Test normal counting")
    # uio_in[1] = oe (1), uio_in[0] = load (0) -> Binary 10 -> Decimal 2
    dut.uio_in.value = 2 
    
    await ClockCycles(dut.clk, 5) 
    # Check value on the falling edge so the output signal is completely stable
    await FallingEdge(dut.clk)
    assert dut.uo_out.value == 5, f"Expected 5, got {int(dut.uo_out.value)}"
    
    # 5. Test the load function
    dut._log.info("Test loading a value (50)")
    dut.ui_in.value = 50
    # uio_in[1] = oe (1), uio_in[0] = load (1) -> Binary 11 -> Decimal 3
    dut.uio_in.value = 3 
    
    await ClockCycles(dut.clk, 1)
    await FallingEdge(dut.clk)
    assert dut.uo_out.value == 50, f"Expected 50, got {int(dut.uo_out.value)}"
    
    # 6. Test counting up from the loaded value
    dut._log.info("Test counting from loaded value")
    dut.uio_in.value = 2 
    
    await ClockCycles(dut.clk, 2)
    await FallingEdge(dut.clk)
    assert dut.uo_out.value == 52, f"Expected 52, got {int(dut.uo_out.value)}"

    # 7. Test output enable disabled (Tri-state)
    dut._log.info("Test output enable disabled (Tri-state)")
    # uio_in[1] = oe (0), uio_in[0] = load (0) -> Binary 00 -> Decimal 0
    dut.uio_in.value = 0 
    
    await ClockCycles(dut.clk, 1)
    await FallingEdge(dut.clk)
    # When output enable is low, the output should be high-impedance ('z')
    assert str(dut.uo_out.value).lower() == 'zzzzzzzz', f"Expected zzzzzzzz, got {str(dut.uo_out.value)}"
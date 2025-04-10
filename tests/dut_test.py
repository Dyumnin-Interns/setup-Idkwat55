import cocotb
from cocotb.triggers import Timer
import random as rnd 
from cocotb_coverage.coverage import CoverPoint, CoverCross, coverage_db

@CoverPoint("top.a",
            xf = lambda x,y:x,
            bins=[0,1]
            )
@CoverPoint("top.b",
            xf = lambda x,y:y,
            bins=[0,1]
            )
@CoverCross("top.cross",
            items=["top.a","top.b"]
            )
def cvr(x,y):
    pass 

@cocotb.test()
async def dut_test(dut):
    for i in range(8):
        av = rnd.randint(0,1) 
        bv = rnd.randint(0,1) 
        dut.a.value=av 
        dut.b.value=bv
        cvr(av,bv)
        await Timer(2, "ns")
        assert dut.y.value.integer == dut.a.value.integer ^ dut.b.value.integer, "Mismatch"

    coverage_db.report_coverage(cocotb.log.warning, bins=True)
    cocotb.log.warning(f"Cross Coverage: {coverage_db["top.cross"].cover_percentage:.4f}")

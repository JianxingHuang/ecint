from ecint.preprocessor.input import InputSetsFromFile
from ecint.preprocessor import path2structure
from aiida.orm import Dict, Code, StructureData
from aiida.plugins import CalculationFactory
from aiida.engine import run

from aiida import load_profile
load_profile()

your_json = 'example.json'
your_structure = 'graphene.xyz'
your_cell = [20, 20, 20]  # 晶胞大小，就是 input.inp 里的 cell
your_pbc = [True, True, True]  # 周期性边界条件，先不用管
your_code = 'cp2k@chenglab51'


class ExampleInputSets(InputSetsFromFile):
    def __init__(self, structure, config=your_json, kind_section_config='DZVPSets'):
        super(ExampleInputSets, self).__init__(structure, config, kind_section_config)


# 生成 cp2k input.inp，不是 cp2k.lsf
input_structure = path2structure(your_structure, your_cell, your_pbc)
eis = ExampleInputSets(input_structure)
total_input_sets = eis.generate_cp2k_input_file()
print(total_input_sets)

# 设定参数，准备提交至服务器
Cp2kCalculation = CalculationFactory('cp2k')
builder = Cp2kCalculation.get_builder()
builder.structure = StructureData(ase=input_structure)
builder.parameters = Dict(dict=eis.input_sets)
builder.code = Code.get_from_string(your_code)
builder.metadata.options.resources = {'tot_num_mpiprocs': 28}
builder.metadata.options.max_wallclock_seconds = 20 * 60
builder.metadata.options.queue_name = 'small'

# 提交至服务器（为了不占用资源，实际上仅生成测试的提交文件，并不真正提交至服务器）
builder.metadata.dry_run = True
print("Submitted calculation...")
run(builder)

from celery import Celery
from dotenv import dotenv_values
import os, tempfile

celery = Celery()

env = dotenv_values()

celery.conf.update(
    broker_url = env.get("CELERY_BROKER_URL"),
    result_backend = env.get("CELERY_RESULT_BACKEND"),
    broker_connection_retry_on_startup = True
)

tempdir = tempfile.TemporaryDirectory(dir=".",prefix="celery_")

@celery.task()
def run_verilog(code,tb):
    code_file = open(tempdir.name+"/code.v","w")
    code_file.write(code)
    code_file.close()
    file1 = tempfile.TemporaryFile(dir=tempdir.name,prefix="")
    file2 = tempfile.TemporaryFile(dir=tempdir.name,prefix="tb_op_")
    os.system(f"iverilog -o {tempdir.name}/op_{file1.name} {tb} {tempdir.name}/code.v")
    os.system(f"vvp {tempdir.name}/op_{file1.name} > {tempdir.name}/tb_op_{file2.name}")
    op = open(f"{tempdir.name}/tb_op_{file2.name}")
    try:
        if op.readlines()[0] != "I give up.":
            return "".join(open(f"{tempdir.name}/tb_op_{file2.name}").readlines()[1:-1])
    except:
        return False

@celery.task()
def create_verilog(code,tb):
    code_file = open(tempdir.name+"/code.v","w")
    code_file.write(code)
    code_file.close()
    tb_file = open(tempdir.name+"/tb.v","w")
    tb_file.write(tb)
    tb_file.close()
    file1 = tempfile.TemporaryFile(dir=tempdir.name,prefix="")
    file2 = tempfile.TemporaryFile(dir=tempdir.name,prefix="tb_op_")
    os.system(f"iverilog -o {tempdir.name}/op_{file1.name} {tempdir.name}/tb.v {tempdir.name}/code.v")
    os.system(f"vvp {tempdir.name}/op_{file1.name} > {tempdir.name}/tb_op_{file2.name}")
    op = open(f"{tempdir.name}/tb_op_{file2.name}")
    try:
        if op.readlines()[0] != "I give up.":
            return "".join(open(f"{tempdir.name}/tb_op_{file2.name}").readlines()[1:-1])
    except:
        return False

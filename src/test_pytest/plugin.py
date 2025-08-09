from _datetime import datetime
import pytest
import requests

data = {"failed":0,
        "success": 0,
        "total":False}
#读取配置文件
def pytest_addoption(parser):
    parser.addini(
        "send_when",
        help="什么时候发送企微信息"
    )
    parser.addini(
        "send_address",
        help="发送的地址"
    )
def pytest_collection_finish(session: pytest.Session) :
    #用例加载完成后执行，包含全部用例
    real_items = [i for i in session.items if i.nodeid.split("::")[-1] != "test_pass"]
    data["total"] += len(real_items)
    print(f'用例的总数是{data["total"]}')

def pytest_configure(config : pytest.Config):
    #配置加载之后,用例执行之前
    data["start_time"] = datetime.now()
    data["send_when"] = config.getini("send_when")
    data["send_address"] = config.getini("send_address")
    print(data["send_address"])

def pytest_runtest_logreport(report : pytest.TestReport):
    #执行每条用例时
    if report.when == "call":
        if report.outcome == "passed" and report.nodeid.split("::")[-1] != "test_pass":
            print(f"本次用例执行结果为{report.outcome}")
            data["success"] += 1
        elif report.nodeid.split("::")[-1] != "test_pass":
            print(f"本次用例执行结果为{report.outcome}")
            data["failed"] += 1

def pytest_unconfigure():
    #测试结束后执行
    data["end_time"] = datetime.now()
    print(f"{datetime.now()}pytest结束执行")

    data["duration"] = (data["end_time"] - data["start_time"]).total_seconds()
    data["pass_retion"] = (data["success"] / (data["failed"]+data["success"]) )* 100
    if data["pass_retion"] >= 100:
        data["pass_retion"] = 100
    else:
        data["pass_retion"] = f'{data["pass_retion"]:.2f}%'



    print(f'运行时长：{data["duration"]}')
    print(f'运行用例总数：{data["total"]}')
    print(f'用例成功数：{data["success"]}')
    print(f'用例失败数：{data["failed"]}')
    print(f'用例成功率：{data["pass_retion"]}%')
    if data["send_when"] == "on_fail" and data["failed"] !=0 and data["send_address"] :
        data["send_tag"] = True
        send_result()



def send_result():


        url = data["send_address"]
        content =f"""
        测试结果：   
        测试时间：{ data["start_time"]}
        用例数量： {data["total"] }
        执行时长： {data["duration"]}s
        测试通过数： {data["success"]}
        测试失败数：<font color=\"warning\">{data["failed"]}</font>
        测试通过率： {data["pass_retion"]}
        测试报告地址： """

        json = {
            "msgtype": "markdown",
            "markdown": {
                "content": content  },

        }

        requests.post(url,json=json)


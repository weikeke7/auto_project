from _datetime import datetime
import pytest
import requests

data = {"failed":0,
        "success": 0}


def pytest_collection_finish(session: pytest.Session) :
    #用例加载完成后执行，包含全部用例
    data["total"] = len(session.items)
    print(f'用例的总数是{data["total"]}')

def pytest_configure():
    #测试开始前执行
    data["start_time"] = datetime.now()
    print(f"{datetime.now()}pytest开始执行")


def pytest_runtest_logreport(report : pytest.TestReport):
    #执行每条用例时
    if report.when == "call":
        if report.outcome == "passed":
            print(f"本次用例执行结果为{report.outcome}")
            data["success"] += 1
        else:
            print(f"本次用例执行结果为{report.outcome}")
            data["failed"] += 1

def pytest_unconfigure():
    #测试结束后执行
    data["end_time"] = datetime.now()
    print(f"{datetime.now()}pytest结束执行")
    data["duration"] = (data["end_time"] - data["start_time"]).total_seconds()



    data["pass_retion"] = data["success"] / data["total"] * 100
    data["pass_retion"] = f'{data["pass_retion"]:.2f}%'



    print(f'运行时长：{data["duration"]}')
    print(f'运行用例总数：{data["total"]}')
    print(f'用例成功数：{data["success"]}')
    print(f'用例失败数：{data["failed"]}')
    print(f'用例成功率时长：{data["pass_retion"]}')

    assert data["duration"]
    assert data["total"] == 3
    assert data["success"] == 2
    assert data["failed"] == 1
    assert data["pass_retion"] == "66.67%"



    #发送测试结果到企业微信

    url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=9967d7b8-8a0d-412d-bded-61b74649bb85'

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
        "mentioned_list":["wangqing","@all"],
    }



    requests.post(url,json=json)
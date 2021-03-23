# -*- coding: utf-8 -*-

#ЗАДАНИЕ 1
#   - Открыть браузер
#   - Очистить кэш браузера
#   - Перейти на https://sbis.ru/ofd
#   - Собрать максимально возможное количество метрик, 
#     характеризующих скорость открытия страницы 

import pychrome as pc
import matplotlib.pyplot as plt
import json
import subprocess

subprocess.Popen("C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir=remote-profile")

BASE_URL = "https://sbis.ru/"
TASK_URL = BASE_URL + "ofd"
WAIT_TIMING = 30 #на меньших интервалах не все тайминги успевали записаться исходя из документации

expressionFetchTimings = "JSON.stringify(window.performance.timing);"

browser = pc.Browser(url="http://127.0.0.1:9222")

tabs = []
collectedTimings = {}
collectedTimings["connectionTiming"] = []
collectedTimings["fullPageLoadTiming"] = []
collectedTimings["domInteractiveTiming"] = []
collectedTimings["domLoadingEventTiming"] = []
collectedTimings["domainLookUpTiming"] = []
collectedTimings["domainLookUpStartSinceNavigationTiming"] = []
collectedTimings["domLoadingUntilFull"] = []

for i in range(10):
    tabs.append(browser.new_tab())

for tab in tabs:
    tab.start()
    tab.Network.enable()
    tab.Network.clearBrowserCache()
    tab.Page.navigate(url=TASK_URL, timeout=WAIT_TIMING)
    print("working tab: ", tab)
    tab.wait(WAIT_TIMING)
    tab.Performance.enable()
    tab.Runtime.enable()
    scriptId = tab.Runtime.compileScript(expression=expressionFetchTimings, sourceURL=TASK_URL, persistScript=True)
    performanceTimingData = json.loads(tab.Runtime.runScript(scriptId=scriptId["scriptId"])["result"]["value"])
    
    collectedTimings["connectionTiming"].append(performanceTimingData["connectEnd"] - performanceTimingData["connectStart"])
    collectedTimings["fullPageLoadTiming"].append(performanceTimingData["loadEventEnd"] - performanceTimingData["navigationStart"])
    collectedTimings["domInteractiveTiming"].append(performanceTimingData["domInteractive"] - performanceTimingData["domLoading"])
    collectedTimings["domLoadingEventTiming"].append(performanceTimingData["domContentLoadedEventEnd"] - performanceTimingData["domContentLoadedEventStart"])
    collectedTimings["domainLookUpTiming"].append(performanceTimingData["domainLookupEnd"] - performanceTimingData["domainLookupStart"])
    collectedTimings["domainLookUpStartSinceNavigationTiming"].append(performanceTimingData["domainLookupStart"] - performanceTimingData["navigationStart"])
    collectedTimings["domLoadingUntilFull"].append(performanceTimingData["loadEventEnd"] - performanceTimingData["domContentLoadedEventStart"])
    
    tab.wait(1)
    tab.stop()
    browser.close_tab(tab)

print(collectedTimings)

times = []
for i in range(10):
    times.append(i)

for currentTiming in collectedTimings:
    plt.plot(times, collectedTimings[currentTiming], label=currentTiming)

plt.xlabel("Nth attempt")
plt.ylabel("Metric value")
plt.title("Page loading metrics")
plt.legend()
plt.show()

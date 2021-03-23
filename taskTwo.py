# -*- coding: utf-8 -*-

#ЗАДАНИЕ 2
#   - Открыть браузер
#   - Очистить кэш браузера
#   - Перейти на https://online.sbis.ru/auth/?ret=%2Fauth
#   - Кликнуть на элемент “ДЕМО”
#   - Кликнуть на элемент “Электронный документооборот”
#   - Перейти на https://online.saby.ru/page/incoming
#   - Кликнуть на первый элемент в списке
#   - Оценить скорость открытия панели (карточки) любым способом

import pychrome as pc
import json
import subprocess

subprocess.Popen("C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir=remote-profile")

LOGIN_URL = "https://online.sbis.ru/auth/?ret=%2Fauth"
INCOMING_PAGE_URL = "https://online.saby.ru/page/incoming"
WAIT_TIMING = 30
DEMO_SELECTOR = "#wasaby-content > div.bodyContent > div.page-Entity__contentWrapper.bodyContent__zIndex-context > div > div.auth-MainContent > div.auth-MainTabs > div > a:nth-child(3)"
ITEM_DOCUMENTS_SELECTOR = "#wasaby-content > div.bodyContent > div.page-Entity__contentWrapper.bodyContent__zIndex-context > div > div.auth-MainContent > div.auth-MainContent__wrapper > div > div > div.controls-Scroll-ContainerBase.controls-Scroll__content_hideNativeScrollbar.controls-Scroll-ContainerBase__scroll_vertical.controls-Scroll__content.controls-Scroll-Container__base.controls-BlockLayout__blockGroup_theme-default.controls-BlockLayout__blockGroup_theme-default > div > div > div:nth-child(2) > div > div.demo-Auth__items > div.demo-Auth__item.documents > div.demo-Auth__item-content > div.demo-Auth__item-title"
ITEM_SELECTOR = "#wasaby-content > div.bodyContent > div.page-Controller.bodyContent__zIndex-context > div.ws-flexbox.ws-flex-column.sabyPage-MainLayout.controls-BlockLayout_background.controls-Popup__dialog-target-container.controls-Popup__stack-target-container.ws-site-width-1024.page-Controller__content > div > div > div.sabyPage-MainLayout__workspaceWrapper.controls-background-default_theme-default.ws-flexbox.ws-flex-column.ws-flex-grow-1.ws-flex-shrink-1 > div.sabyPage-MainLayout__workspace.ws-flexbox.ws-flex-grow-1.ws-flex-shrink-1.ws-flex-column > div.sabyPage-MainLayout__middle.ws-flex-shrink-1.ws-flexbox > div > div.edws-fullHeight.edws-fullWidth.controls-MasterDetail_details.controls-MasterDetail_details_bg-contrast_theme-default > div > div > div > div.layout-Browser.edo3-Browser-browser > div.layout-Browser__content.layout-Browser__content_theme-default"

expressionFetchTimings = "JSON.stringify(window.performance.timing);"

browser = pc.Browser(url="http://127.0.0.1:9222")

#@param tab: tab to work with
#@param xCoord: x coordinate in css pixels (cdp docs)
#@param yCoord: y coordinate in css pixels (cdp docs)
def mouseClick(tab, xCoord, yCoord):
    tab.call_method("Input.dispatchMouseEvent", type="mousePressed", x=xCoord, y=yCoord, button="left", clickCount=1)
    tab.call_method("Input.dispatchMouseEvent", type="mouseReleased", x=xCoord, y=yCoord, button="left", clickCount=1)

tab = browser.new_tab()
tab.start()
tab.Network.enable()
tab.Network.clearBrowserCache()
tab.Page.navigate(url=LOGIN_URL, timeout=5)
tab.wait(5)
tab.Performance.enable()
tab.Runtime.enable()
tab.call_method("DOM.enable")
rootId = tab.call_method("DOM.getDocument")["root"]["nodeId"]

nodeId = tab.call_method("DOM.querySelector", nodeId=rootId, selector=DEMO_SELECTOR)["nodeId"]

demoBoxModel = tab.call_method("DOM.getBoxModel", nodeId=nodeId)["model"]["content"]

mouseClick(tab, demoBoxModel[0], demoBoxModel[1])
tab.wait(5)
itemDocumentsNodeId = tab.call_method("DOM.querySelector", nodeId=rootId, selector=ITEM_DOCUMENTS_SELECTOR)["nodeId"]

tab.call_method("DOM.scrollIntoViewIfNeeded", nodeId=itemDocumentsNodeId)
tab.wait(1)
itemDocumentsBoxModel = tab.call_method("DOM.getBoxModel", nodeId=itemDocumentsNodeId)["model"]["content"]

mouseClick(tab, itemDocumentsBoxModel[0], itemDocumentsBoxModel[1])

tab.wait(5)
tab.Page.navigate(url=INCOMING_PAGE_URL, timeout=20)
tab.wait(20)
rootId = tab.call_method("DOM.getDocument")["root"]["nodeId"]

itemNodeId = tab.call_method("DOM.querySelector", nodeId=rootId, selector="#wasaby-content > div.bodyContent > div.page-Controller.bodyContent__zIndex-context")
linkId = tab.call_method("DOM.querySelector", nodeId=itemNodeId["nodeId"], selector="#wasaby-content > div.bodyContent > div.page-Controller.bodyContent__zIndex-context > div.ws-flexbox.ws-flex-column.sabyPage-MainLayout.controls-BlockLayout_background.controls-Popup__dialog-target-container.controls-Popup__stack-target-container.ws-site-width-1536.page-Controller__content > div > div.sabyPage-MainLayout__mainContent.controls-BlockLayout__block_theme-default.ws-flexbox.ws-flex-shrink-1.ws-flex-grow-1.ws-flex-row > div.sabyPage-MainLayout__workspaceWrapper.controls-background-default_theme-default.ws-flexbox.ws-flex-column.ws-flex-grow-1.ws-flex-shrink-1 > div.sabyPage-MainLayout__workspace.ws-flexbox.ws-flex-grow-1.ws-flex-shrink-1.ws-flex-column > div.sabyPage-MainLayout__middle.ws-flex-shrink-1.ws-flexbox")
dataId = tab.call_method("DOM.querySelector", nodeId=linkId["nodeId"], selector="#wasaby-content > div.bodyContent > div.page-Controller.bodyContent__zIndex-context > div.ws-flexbox.ws-flex-column.sabyPage-MainLayout.controls-BlockLayout_background.controls-Popup__dialog-target-container.controls-Popup__stack-target-container.ws-site-width-1536.page-Controller__content > div > div.sabyPage-MainLayout__mainContent.controls-BlockLayout__block_theme-default.ws-flexbox.ws-flex-shrink-1.ws-flex-grow-1.ws-flex-row > div.sabyPage-MainLayout__workspaceWrapper.controls-background-default_theme-default.ws-flexbox.ws-flex-column.ws-flex-grow-1.ws-flex-shrink-1 > div.sabyPage-MainLayout__workspace.ws-flexbox.ws-flex-grow-1.ws-flex-shrink-1.ws-flex-column > div.sabyPage-MainLayout__middle.ws-flex-shrink-1.ws-flexbox > div > div.edws-fullHeight.edws-fullWidth.controls-MasterDetail_details.controls-MasterDetail_details_bg-contrast_theme-default > div > div > div > div.layout-Browser.edo3-Browser-browser > div.layout-Browser__content.layout-Browser__content_theme-default")

dataBoxModel = tab.call_method("DOM.getBoxModel", nodeId=dataId["nodeId"])["model"]["content"]

mouseClick(tab, dataBoxModel[0] + 200, dataBoxModel[1])

tab.wait(20)

scriptId = tab.Runtime.compileScript(expression=expressionFetchTimings, sourceURL=INCOMING_PAGE_URL, persistScript=True)
performanceTimingData = json.loads(tab.Runtime.runScript(scriptId=scriptId["scriptId"])["result"]["value"])

collectedTimings = {}

collectedTimings["connectionTiming"] = (performanceTimingData["connectEnd"] - performanceTimingData["connectStart"])
collectedTimings["fullPageLoadTiming"] = (performanceTimingData["loadEventEnd"] - performanceTimingData["navigationStart"])
collectedTimings["domInteractiveTiming"] = (performanceTimingData["domInteractive"] - performanceTimingData["domLoading"])
collectedTimings["domLoadingEventTiming"] = (performanceTimingData["domContentLoadedEventEnd"] - performanceTimingData["domContentLoadedEventStart"])
collectedTimings["domainLookUpTiming"] = (performanceTimingData["domainLookupEnd"] - performanceTimingData["domainLookupStart"])
collectedTimings["domainLookUpStartSinceNavigationTiming"] = (performanceTimingData["domainLookupStart"] - performanceTimingData["navigationStart"])
collectedTimings["domLoadingUntilFull"] = (performanceTimingData["loadEventEnd"] - performanceTimingData["domContentLoadedEventStart"])
tab.stop()
browser.close_tab(tab)

print("Timings in ms since card loading")
print(collectedTimings)

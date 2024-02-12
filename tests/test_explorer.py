import os
import sys

import pytest
from PyQt5 import QtCore, QtGui, QtTest, QtWidgets, uic
from PyQt5.QtCore import QCoreApplication, QObject, Qt, QDir, QUrl
from PyQt5.QtWidgets import *
from pytestqt.plugin import QtBot
from PyQt5.QtGui import QDesktopServices

GUI = __import__("explorer")


@pytest.fixture(scope="module")
def qtbot_session(qapp, request):
    print("  SETUP qtbot")
    result = QtBot(qapp)
    with capture_exceptions() as exceptions:
        yield result
    print("  TEARDOWN qtbot")


@pytest.fixture(scope="module")
def Viewer(request):
    print("  SETUP GUI")

    app, imageViewer = GUI.main_GUI()
    qtbotbis = QtBot(app)
    QtTest.QTest.qWait(1000)

    return  app, imageViewer, qtbotbis

def test_load(Viewer):
    app, imageViewer, qtbot = Viewer

    assert imageViewer.directPath.text() != ''

def test_toInputDir(Viewer):
    app, imageViewer, qtbot = Viewer
    curDir = QDir.current()
    before = imageViewer.dirContent.model().rowCount()
    if not curDir.exists('test'):
        curDir.mkdir('test')
        after = imageViewer.dirContent.model().rowCount()
        curDir.rmdir('test')

        assert before != after
    else:
        assert False

#def test_rootUp(Viewer):
#    app, imageViewer, qtbot = Viewer
#    curDir = QDir.cd("C:/")
#    if curDir:
#        imageViewer.upperDirect()
#


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'project_fab_windows.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QListView, QMainWindow, QMenu, QMenuBar,
    QPlainTextEdit, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1030, 821)
        MainWindow.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_root = QVBoxLayout(self.centralwidget)
        self.verticalLayout_root.setSpacing(10)
        self.verticalLayout_root.setObjectName(u"verticalLayout_root")
        self.grpProfile = QGroupBox(self.centralwidget)
        self.grpProfile.setObjectName(u"grpProfile")
        self.gridLayout_profile = QGridLayout(self.grpProfile)
        self.gridLayout_profile.setObjectName(u"gridLayout_profile")
        self.cmbProfile = QComboBox(self.grpProfile)
        self.cmbProfile.setObjectName(u"cmbProfile")

        self.gridLayout_profile.addWidget(self.cmbProfile, 0, 1, 1, 1)

        self.btnNewProfile = QPushButton(self.grpProfile)
        self.btnNewProfile.setObjectName(u"btnNewProfile")

        self.gridLayout_profile.addWidget(self.btnNewProfile, 0, 2, 1, 1)

        self.btnSaveProfile = QPushButton(self.grpProfile)
        self.btnSaveProfile.setObjectName(u"btnSaveProfile")

        self.gridLayout_profile.addWidget(self.btnSaveProfile, 0, 4, 1, 1)

        self.lblProfile = QLabel(self.grpProfile)
        self.lblProfile.setObjectName(u"lblProfile")

        self.gridLayout_profile.addWidget(self.lblProfile, 0, 0, 1, 1)

        self.btnRenameProfile = QPushButton(self.grpProfile)
        self.btnRenameProfile.setObjectName(u"btnRenameProfile")

        self.gridLayout_profile.addWidget(self.btnRenameProfile, 0, 3, 1, 1)


        self.verticalLayout_root.addWidget(self.grpProfile)

        self.grpProject = QGroupBox(self.centralwidget)
        self.grpProject.setObjectName(u"grpProject")
        self.gridLayout_project = QGridLayout(self.grpProject)
        self.gridLayout_project.setObjectName(u"gridLayout_project")
        self.lblTemplate = QLabel(self.grpProject)
        self.lblTemplate.setObjectName(u"lblTemplate")

        self.gridLayout_project.addWidget(self.lblTemplate, 0, 0, 1, 1)

        self.edTemplate = QLineEdit(self.grpProject)
        self.edTemplate.setObjectName(u"edTemplate")

        self.gridLayout_project.addWidget(self.edTemplate, 0, 1, 1, 1)

        self.btnBrowseTemplate = QPushButton(self.grpProject)
        self.btnBrowseTemplate.setObjectName(u"btnBrowseTemplate")

        self.gridLayout_project.addWidget(self.btnBrowseTemplate, 0, 2, 1, 1)

        self.lblOut = QLabel(self.grpProject)
        self.lblOut.setObjectName(u"lblOut")

        self.gridLayout_project.addWidget(self.lblOut, 1, 0, 1, 1)

        self.edOut = QLineEdit(self.grpProject)
        self.edOut.setObjectName(u"edOut")

        self.gridLayout_project.addWidget(self.edOut, 1, 1, 1, 1)

        self.btnBrowseOut = QPushButton(self.grpProject)
        self.btnBrowseOut.setObjectName(u"btnBrowseOut")

        self.gridLayout_project.addWidget(self.btnBrowseOut, 1, 2, 1, 1)

        self.lblPattern = QLabel(self.grpProject)
        self.lblPattern.setObjectName(u"lblPattern")

        self.gridLayout_project.addWidget(self.lblPattern, 2, 0, 1, 1)

        self.edPattern = QLineEdit(self.grpProject)
        self.edPattern.setObjectName(u"edPattern")

        self.gridLayout_project.addWidget(self.edPattern, 2, 1, 1, 2)


        self.verticalLayout_root.addWidget(self.grpProject)

        self.grpPlugins = QGroupBox(self.centralwidget)
        self.grpPlugins.setObjectName(u"grpPlugins")
        self.verticalLayout = QVBoxLayout(self.grpPlugins)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_2 = QLabel(self.grpPlugins)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.listPlugins = QListView(self.grpPlugins)
        self.listPlugins.setObjectName(u"listPlugins")

        self.verticalLayout_3.addWidget(self.listPlugins)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.lblExcludeFolders = QLabel(self.grpPlugins)
        self.lblExcludeFolders.setObjectName(u"lblExcludeFolders")

        self.verticalLayout_2.addWidget(self.lblExcludeFolders)

        self.listFolders = QListView(self.grpPlugins)
        self.listFolders.setObjectName(u"listFolders")
        self.listFolders.setMinimumSize(QSize(0, 140))

        self.verticalLayout_2.addWidget(self.listFolders)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.verticalLayout_root.addWidget(self.grpPlugins)

        self.grpVersions = QGroupBox(self.centralwidget)
        self.grpVersions.setObjectName(u"grpVersions")
        self.gridLayout_versions = QGridLayout(self.grpVersions)
        self.gridLayout_versions.setObjectName(u"gridLayout_versions")
        self.listVersions = QListView(self.grpVersions)
        self.listVersions.setObjectName(u"listVersions")

        self.gridLayout_versions.addWidget(self.listVersions, 1, 0, 1, 2)

        self.lblVersions = QLabel(self.grpVersions)
        self.lblVersions.setObjectName(u"lblVersions")

        self.gridLayout_versions.addWidget(self.lblVersions, 0, 0, 1, 1)


        self.verticalLayout_root.addWidget(self.grpVersions)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btnBuild = QPushButton(self.centralwidget)
        self.btnBuild.setObjectName(u"btnBuild")

        self.horizontalLayout.addWidget(self.btnBuild)

        self.btnCancel = QPushButton(self.centralwidget)
        self.btnCancel.setObjectName(u"btnCancel")
        self.btnCancel.setEnabled(False)

        self.horizontalLayout.addWidget(self.btnCancel)

        self.horizontalSpacer_actions = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_actions)

        self.btnOpenOut = QPushButton(self.centralwidget)
        self.btnOpenOut.setObjectName(u"btnOpenOut")

        self.horizontalLayout.addWidget(self.btnOpenOut)


        self.verticalLayout_root.addLayout(self.horizontalLayout)

        self.vLayout_feedback = QVBoxLayout()
        self.vLayout_feedback.setObjectName(u"vLayout_feedback")
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(True)

        self.vLayout_feedback.addWidget(self.progressBar)

        self.txtLogs = QPlainTextEdit(self.centralwidget)
        self.txtLogs.setObjectName(u"txtLogs")
        self.txtLogs.setReadOnly(True)

        self.vLayout_feedback.addWidget(self.txtLogs)


        self.verticalLayout_root.addLayout(self.vLayout_feedback)

        self.footerFrame = QFrame(self.centralwidget)
        self.footerFrame.setObjectName(u"footerFrame")
        self.footerFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.hLayout_footer = QHBoxLayout(self.footerFrame)
        self.hLayout_footer.setObjectName(u"hLayout_footer")
        self.spacer_footer_left = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hLayout_footer.addItem(self.spacer_footer_left)

        self.lblFooter = QLabel(self.footerFrame)
        self.lblFooter.setObjectName(u"lblFooter")
        self.lblFooter.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.hLayout_footer.addWidget(self.lblFooter)

        self.spacer_footer_right = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hLayout_footer.addItem(self.spacer_footer_right)


        self.verticalLayout_root.addWidget(self.footerFrame)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1030, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuTheme = QMenu(self.menubar)
        self.menuTheme.setObjectName(u"menuTheme")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTheme.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionAbout)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"UE5 Fab Zip Tools", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About ", None))
        self.grpProfile.setTitle(QCoreApplication.translate("MainWindow", u"Profil", None))
        self.btnNewProfile.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.btnSaveProfile.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.lblProfile.setText(QCoreApplication.translate("MainWindow", u"Active profile :", None))
        self.btnRenameProfile.setText(QCoreApplication.translate("MainWindow", u"Rename", None))
        self.grpProject.setTitle(QCoreApplication.translate("MainWindow", u"Project", None))
        self.lblTemplate.setText(QCoreApplication.translate("MainWindow", u"UE5 Project Folder:", None))
        self.edTemplate.setPlaceholderText(QCoreApplication.translate("MainWindow", u"/path/to/my/ue_project", None))
        self.btnBrowseTemplate.setText(QCoreApplication.translate("MainWindow", u"Browse...", None))
        self.lblOut.setText(QCoreApplication.translate("MainWindow", u"Output folder:", None))
        self.edOut.setPlaceholderText(QCoreApplication.translate("MainWindow", u"/path/to/output", None))
        self.btnBrowseOut.setText(QCoreApplication.translate("MainWindow", u"Browse...", None))
        self.lblPattern.setText(QCoreApplication.translate("MainWindow", u"ZIP Naming:", None))
#if QT_CONFIG(tooltip)
        self.edPattern.setToolTip(QCoreApplication.translate("MainWindow", u"{project} = nom du projet, {ueversion} = 5.x, {date} = AAAAMMJJ_HHMMSS", None))
#endif // QT_CONFIG(tooltip)
        self.edPattern.setText(QCoreApplication.translate("MainWindow", u"{project}_UE{ueversion}", None))
        self.grpPlugins.setTitle(QCoreApplication.translate("MainWindow", u"Plugins / Sub Folders", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Plugins in .uproject to exclude in ZIP", None))
        self.lblExcludeFolders.setText(QCoreApplication.translate("MainWindow", u"Extra Files/Folders to exclude in ZIP", None))
        self.grpVersions.setTitle(QCoreApplication.translate("MainWindow", u"UE Versions", None))
        self.lblVersions.setText(QCoreApplication.translate("MainWindow", u"Select the versions to package:", None))
        self.btnBuild.setText(QCoreApplication.translate("MainWindow", u"Zip - UE5 Project Versions", None))
        self.btnCancel.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
        self.btnOpenOut.setText(QCoreApplication.translate("MainWindow", u"Open Output Folder", None))
        self.lblFooter.setText(QCoreApplication.translate("MainWindow", u"Copyright \u00a9 SCHARTIER Isaac trading as Somndus Studio", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuTheme.setTitle(QCoreApplication.translate("MainWindow", u"Theme", None))
    # retranslateUi


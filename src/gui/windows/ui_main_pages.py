# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_pages.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QListView,
    QPlainTextEdit, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QStackedWidget, QVBoxLayout, QWidget)

class Ui_MainPages(object):
    def setupUi(self, MainPages):
        if not MainPages.objectName():
            MainPages.setObjectName(u"MainPages")
        MainPages.resize(1030, 792)
        MainPages.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))
        self.main_pages_layout = QVBoxLayout(MainPages)
        self.main_pages_layout.setSpacing(0)
        self.main_pages_layout.setObjectName(u"main_pages_layout")
        self.main_pages_layout.setContentsMargins(5, 5, 5, 5)
        self.pages = QStackedWidget(MainPages)
        self.pages.setObjectName(u"pages")
        self.page_1 = QWidget()
        self.page_1.setObjectName(u"page_1")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.page_1.sizePolicy().hasHeightForWidth())
        self.page_1.setSizePolicy(sizePolicy)
        self.verticalLayout_root = QVBoxLayout(self.page_1)
        self.verticalLayout_root.setSpacing(10)
        self.verticalLayout_root.setObjectName(u"verticalLayout_root")
        self.grpProfile = QGroupBox(self.page_1)
        self.grpProfile.setObjectName(u"grpProfile")
        self.gridLayout_profile = QGridLayout(self.grpProfile)
        self.gridLayout_profile.setObjectName(u"gridLayout_profile")
        self.p1_profile_row_1_layout = QHBoxLayout()
        self.p1_profile_row_1_layout.setObjectName(u"p1_profile_row_1_layout")
        self.lblProfile = QLabel(self.grpProfile)
        self.lblProfile.setObjectName(u"lblProfile")

        self.p1_profile_row_1_layout.addWidget(self.lblProfile)

        self.cmbProfile = QComboBox(self.grpProfile)
        self.cmbProfile.setObjectName(u"cmbProfile")
        self.cmbProfile.setMinimumSize(QSize(400, 0))

        self.p1_profile_row_1_layout.addWidget(self.cmbProfile)

        self.btnNewProfile = QPushButton(self.grpProfile)
        self.btnNewProfile.setObjectName(u"btnNewProfile")

        self.p1_profile_row_1_layout.addWidget(self.btnNewProfile)

        self.btnRenameProfile = QPushButton(self.grpProfile)
        self.btnRenameProfile.setObjectName(u"btnRenameProfile")

        self.p1_profile_row_1_layout.addWidget(self.btnRenameProfile)

        self.btnRemoveProfile = QPushButton(self.grpProfile)
        self.btnRemoveProfile.setObjectName(u"btnRemoveProfile")

        self.p1_profile_row_1_layout.addWidget(self.btnRemoveProfile)

        self.btnSaveProfile = QPushButton(self.grpProfile)
        self.btnSaveProfile.setObjectName(u"btnSaveProfile")

        self.p1_profile_row_1_layout.addWidget(self.btnSaveProfile)


        self.gridLayout_profile.addLayout(self.p1_profile_row_1_layout, 0, 0, 1, 1)


        self.verticalLayout_root.addWidget(self.grpProfile)

        self.grpProject = QGroupBox(self.page_1)
        self.grpProject.setObjectName(u"grpProject")
        self.gridLayout_project = QGridLayout(self.grpProject)
        self.gridLayout_project.setObjectName(u"gridLayout_project")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lblTemplate = QLabel(self.grpProject)
        self.lblTemplate.setObjectName(u"lblTemplate")
        self.lblTemplate.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_3.addWidget(self.lblTemplate)

        self.edTemplate = QLineEdit(self.grpProject)
        self.edTemplate.setObjectName(u"edTemplate")

        self.horizontalLayout_3.addWidget(self.edTemplate)

        self.btnBrowseTemplate = QPushButton(self.grpProject)
        self.btnBrowseTemplate.setObjectName(u"btnBrowseTemplate")

        self.horizontalLayout_3.addWidget(self.btnBrowseTemplate)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.lblOut = QLabel(self.grpProject)
        self.lblOut.setObjectName(u"lblOut")
        self.lblOut.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_5.addWidget(self.lblOut)

        self.edOut = QLineEdit(self.grpProject)
        self.edOut.setObjectName(u"edOut")

        self.horizontalLayout_5.addWidget(self.edOut)

        self.btnBrowseOut = QPushButton(self.grpProject)
        self.btnBrowseOut.setObjectName(u"btnBrowseOut")

        self.horizontalLayout_5.addWidget(self.btnBrowseOut)


        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.lblPattern = QLabel(self.grpProject)
        self.lblPattern.setObjectName(u"lblPattern")
        self.lblPattern.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_7.addWidget(self.lblPattern)

        self.edPattern = QLineEdit(self.grpProject)
        self.edPattern.setObjectName(u"edPattern")

        self.horizontalLayout_7.addWidget(self.edPattern)

        self.horizontalSpacer = QSpacerItem(93, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer)


        self.verticalLayout_4.addLayout(self.horizontalLayout_7)


        self.gridLayout_project.addLayout(self.verticalLayout_4, 0, 0, 1, 1)


        self.verticalLayout_root.addWidget(self.grpProject)

        self.grpPlugins = QGroupBox(self.page_1)
        self.grpPlugins.setObjectName(u"grpPlugins")
        self.verticalLayout = QVBoxLayout(self.grpPlugins)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_2 = QLabel(self.grpPlugins)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)

        self.verticalLayout_3.addWidget(self.label_2)

        self.listPlugins = QListView(self.grpPlugins)
        self.listPlugins.setObjectName(u"listPlugins")

        self.verticalLayout_3.addWidget(self.listPlugins)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.lblExcludeFolders = QLabel(self.grpPlugins)
        self.lblExcludeFolders.setObjectName(u"lblExcludeFolders")
        sizePolicy1.setHeightForWidth(self.lblExcludeFolders.sizePolicy().hasHeightForWidth())
        self.lblExcludeFolders.setSizePolicy(sizePolicy1)

        self.verticalLayout_2.addWidget(self.lblExcludeFolders)

        self.listFolders = QListView(self.grpPlugins)
        self.listFolders.setObjectName(u"listFolders")
        self.listFolders.setMinimumSize(QSize(0, 0))

        self.verticalLayout_2.addWidget(self.listFolders)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.verticalLayout_root.addWidget(self.grpPlugins)

        self.grpVersions = QGroupBox(self.page_1)
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
        self.btnBuild = QPushButton(self.page_1)
        self.btnBuild.setObjectName(u"btnBuild")

        self.horizontalLayout.addWidget(self.btnBuild)

        self.btnCancel = QPushButton(self.page_1)
        self.btnCancel.setObjectName(u"btnCancel")
        self.btnCancel.setEnabled(False)

        self.horizontalLayout.addWidget(self.btnCancel)

        self.horizontalSpacer_actions = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_actions)

        self.btnOpenOut = QPushButton(self.page_1)
        self.btnOpenOut.setObjectName(u"btnOpenOut")

        self.horizontalLayout.addWidget(self.btnOpenOut)


        self.verticalLayout_root.addLayout(self.horizontalLayout)

        self.vLayout_feedback = QVBoxLayout()
        self.vLayout_feedback.setObjectName(u"vLayout_feedback")
        self.progressBar = QProgressBar(self.page_1)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(True)

        self.vLayout_feedback.addWidget(self.progressBar)

        self.txtLogs = QPlainTextEdit(self.page_1)
        self.txtLogs.setObjectName(u"txtLogs")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.txtLogs.sizePolicy().hasHeightForWidth())
        self.txtLogs.setSizePolicy(sizePolicy2)
        self.txtLogs.setReadOnly(True)

        self.vLayout_feedback.addWidget(self.txtLogs)


        self.verticalLayout_root.addLayout(self.vLayout_feedback)

        self.pages.addWidget(self.page_1)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.page_2_layout = QVBoxLayout(self.page_2)
        self.page_2_layout.setSpacing(5)
        self.page_2_layout.setObjectName(u"page_2_layout")
        self.page_2_layout.setContentsMargins(5, 5, 5, 5)
        self.label = QLabel(self.page_2)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(22)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.page_2_layout.addWidget(self.label)

        self.pages.addWidget(self.page_2)

        self.main_pages_layout.addWidget(self.pages)


        self.retranslateUi(MainPages)

        self.pages.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainPages)
    # setupUi

    def retranslateUi(self, MainPages):
        MainPages.setWindowTitle(QCoreApplication.translate("MainPages", u"UE5 Fab Zip Tools", None))
        self.grpProfile.setTitle(QCoreApplication.translate("MainPages", u"Profil", None))
        self.lblProfile.setText(QCoreApplication.translate("MainPages", u"Active profile :", None))
        self.btnNewProfile.setText(QCoreApplication.translate("MainPages", u"New", None))
        self.btnRenameProfile.setText(QCoreApplication.translate("MainPages", u"Rename", None))
        self.btnRemoveProfile.setText(QCoreApplication.translate("MainPages", u"Remove", None))
        self.btnSaveProfile.setText(QCoreApplication.translate("MainPages", u"Save", None))
        self.grpProject.setTitle(QCoreApplication.translate("MainPages", u"Project", None))
        self.lblTemplate.setText(QCoreApplication.translate("MainPages", u"UE5 Project Folder:", None))
        self.edTemplate.setPlaceholderText(QCoreApplication.translate("MainPages", u"/path/to/my/ue_project", None))
        self.btnBrowseTemplate.setText(QCoreApplication.translate("MainPages", u"Browse...", None))
        self.lblOut.setText(QCoreApplication.translate("MainPages", u"Output folder:", None))
        self.edOut.setPlaceholderText(QCoreApplication.translate("MainPages", u"/path/to/output", None))
        self.btnBrowseOut.setText(QCoreApplication.translate("MainPages", u"Browse...", None))
        self.lblPattern.setText(QCoreApplication.translate("MainPages", u"ZIP Naming:", None))
#if QT_CONFIG(tooltip)
        self.edPattern.setToolTip(QCoreApplication.translate("MainPages", u"{project} = nom du projet, {ueversion} = 5.x, {date} =\n"
"                                                        AAAAMMJJ_HHMMSS\n"
"                                                    ", None))
#endif // QT_CONFIG(tooltip)
        self.edPattern.setText(QCoreApplication.translate("MainPages", u"{project}_UE{ueversion}", None))
        self.grpPlugins.setTitle(QCoreApplication.translate("MainPages", u"Plugins / Sub Folders", None))
        self.label_2.setText(QCoreApplication.translate("MainPages", u"Plugins in .uproject to exclude in ZIP\n"
"                                                                    ", None))
        self.lblExcludeFolders.setText(QCoreApplication.translate("MainPages", u"Extra Files/Folders to exclude in ZIP\n"
"                                                                    ", None))
        self.grpVersions.setTitle(QCoreApplication.translate("MainPages", u"UE Versions", None))
        self.lblVersions.setText(QCoreApplication.translate("MainPages", u"Select the versions to package:", None))
        self.btnBuild.setText(QCoreApplication.translate("MainPages", u"Zip - UE5 Project Versions", None))
        self.btnCancel.setText(QCoreApplication.translate("MainPages", u"Cancel", None))
        self.btnOpenOut.setText(QCoreApplication.translate("MainPages", u"Open Output Folder", None))
        self.label.setText(QCoreApplication.translate("MainPages", u"Plugins Builds in Construction", None))
    # retranslateUi


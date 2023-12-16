
import QtQuick 2.3
import QtQuick.Controls 2.2
import QtQuick.Controls.Material 2.2
import QtQuick.Layouts 1.3
import fr.enac.IvyBus 1.0
import fr.enac.IntruderModel 1.0

ColumnLayout {
    Layout.fillWidth: true
    id: intruderLayout
    property string alertMsg: ""

    RowLayout {
        Layout.fillWidth: true

        Label {
            Layout.leftMargin: 10
            font.bold: true
            font.pointSize: 10
            text: qsTr("Intruder Model:")
        }

        Label {
            Layout.leftMargin: 10
            font.pointSize: 10
            text: IntruderModel.connected ? "Running" : "Not running"
        }

        Label {
            Layout.fillWidth: true
            Layout.leftMargin: 10
            font.pointSize: 10
            text: "(" + IntruderModel.position + ")"
        }

        Button {
            Layout.rightMargin: 5
            Layout.alignment: Qt.AlignRight | Qt.AlignTop

            text: qsTr("Reset")
            highlighted: true
            Material.accent: Material.Red
            enabled: IntruderModel.connected
            onClicked: {
                IntruderModel.reset()
            }
        }

        Dialog {
            id: alertDialog
            width: 400
            height: 150
            x: 100
            title: "Alert"
            contentItem: Label {
                text: alertMsg
            }
            standardButtons: Dialog.Ok
        }
    }

    ColumnLayout {
        Layout.fillWidth: true

        TabBar {
            Layout.fillWidth: true
            id: intruBar

            TabButton {
                text: qsTr("Set Intruder Pos")
            }
            TabButton {
                text: qsTr("Set Intruder Conflict")
            }
        }

        StackLayout {
            anchors.margins: margin
            currentIndex: intruBar.currentIndex

            RowLayout {
                TextField {
                    Layout.preferredWidth: 80
                    id: intruX
                    placeholderText: qsTr("X")
                    validator: DoubleValidator{decimals: 2}
                }

                TextField {
                    Layout.preferredWidth: 80
                    id: intruY
                    placeholderText: qsTr("Y")
                    validator: DoubleValidator{decimals: 2}
                }

                TextField {
                    Layout.preferredWidth: 80
                    id: intruZ
                    placeholderText: qsTr("Z")
                    validator: DoubleValidator{decimals: 2}
                }

                TextField {
                    Layout.preferredWidth: 90
                    id: intruVp
                    placeholderText: qsTr("Vp")
                    validator: DoubleValidator{decimals: 2}
                }

                TextField {
                    Layout.preferredWidth: 90
                    id: intruPsi
                    placeholderText: qsTr("Psi")
                    validator: DoubleValidator{decimals: 2}
                }

                Button {
                    text: qsTr("Set")
                    highlighted: true
                    Material.accent: Material.Green
                    enabled: IntruderModel.connected
                    onClicked: {
                        if (intruX.text == "" || intruY.text == "" || intruZ.text == "" || intruVp.text == "" || intruPsi.text == "") {
                            alertMsg = "You have to fullfill all fields to set intruder position";
                            alertDialog.open();
                            return;
                        }
                        IntruderModel.setPosition(intruX.text, intruY.text, intruZ.text, intruVp.text, intruPsi.text);
                    }
                }
            }

            RowLayout {
                TextField {
                    Layout.preferredWidth: 80
                    id: intruTcpa
                    placeholderText: qsTr("tcpa")
                    validator: DoubleValidator{decimals: 2}
                }

                TextField {
                    Layout.preferredWidth: 80
                    id: intruDcpa
                    placeholderText: qsTr("dcpa")
                    validator: DoubleValidator{decimals: 2}
                }

                TextField {
                    Layout.preferredWidth: 80
                    id: intruR0
                    placeholderText: qsTr("r0")
                    validator: DoubleValidator{decimals: 2}
                }

                TextField {
                    Layout.preferredWidth: 100
                    id: intruDeltaTrk
                    placeholderText: qsTr("delta track")
                    validator: DoubleValidator{decimals: 2}
                }

                Button {
                    text: qsTr("Set")
                    highlighted: true
                    Material.accent: Material.Green
                    enabled: IntruderModel.connected
                    onClicked: {
                        if (intruTcpa.text == "" || intruDcpa.text == "" || intruR0.text == "" || intruDeltaTrk.text == "") {
                            alertMsg = "You have to fullfill all fields to init conflict position";
                            alertDialog.open();
                            return;
                        }
                        IntruderModel.initConflictPosition(intruTcpa.text, intruDcpa.text, intruR0.text, intruDeltaTrk.text);
                    }
                }
            }
        }
    }
}

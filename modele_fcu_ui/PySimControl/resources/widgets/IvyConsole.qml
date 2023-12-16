
import QtQuick 2.3
import QtQuick.Controls 2.2
import QtQuick.Controls.Material 2.2
import QtQuick.Dialogs 1.2
import QtQuick.Layouts 1.1
import fr.enac.IvyBus 1.0


ColumnLayout {
    anchors.margins: margin
    Layout.fillWidth: true
    Layout.fillHeight: true

    RowLayout {
        Layout.fillWidth: true

        Button {
            text: qsTr("Clear")
            highlighted: true
            Material.accent: Material.Red
            onClicked: {
                IvyBus.clear();
            }
        }

        Button {
            text: IvyBus.log_recording ? qsTr("Recording...") :
            qsTr("Start recording")
            enabled: !IvyBus.log_recording
            onClicked: {
                IvyBus.record(true);
            }
        }

        Button {
            text: qsTr("Stop recording")
            enabled: IvyBus.log_recording
            onClicked: {
                IvyBus.record(false);
            }
        }
    }

    Rectangle {
        Layout.fillWidth: true
        Layout.fillHeight: true
        color: "#ffffff"
        border.width: 2
        border.color: IvyBus.log_recording ? "steelblue" : "#ccc"
        radius: 3

        ScrollView {
            anchors.fill: parent
            anchors.margins: margin

            TextArea {
                anchors.fill: parent
                textFormat: TextEdit.RichText
                text: IvyBus.log
                readOnly: true
            }
        }
    }
    RowLayout {
        Layout.fillWidth: true

        Label {
            id: ivySendLabel
            text: qsTr("Send message")
            font.pointSize: 12
        }

        TextField {
            id: ivySendMsgInput
            Layout.fillWidth: true
        }

        Button {
            text: qsTr("Send")
            enabled: ivySendMsgInput != ""
            onClicked: {
                IvyBus.send_msg(ivySendMsgInput.text);
                statusLabel.text = qsTr("Message has been sent");
                delay(function() {
                    statusLabel.text = "";
                }, 3000);
            }
        }
    }
}
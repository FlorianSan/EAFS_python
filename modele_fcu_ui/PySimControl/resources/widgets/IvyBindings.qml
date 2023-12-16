
import QtQuick 2.3
import QtQuick.Controls 2.2
import QtQuick.Dialogs 1.2
import QtQuick.Layouts 1.1
import fr.enac.IvyBus 1.0

RowLayout {
    anchors.margins: margin
    Layout.fillWidth: true
    Layout.fillHeight: true
    Layout.alignment: Qt.AlignLeft | Qt.AlignTop

    ColumnLayout {
        Layout.fillHeight: true

        Label {
            id: applicationListLabel
            text: "Connected applications"
            font.pointSize: 11
        }

        Rectangle {
            Layout.fillHeight: true
            width: applicationListLabel.width+10
            color: "#fff"
            border.width: 2
            border.color: "#ccc"
            radius: 3

            // Item used to display an application name
            Component {
                id: applicationName
                Item {
                    width: applicationListView.width
                    height: 20
                    Text {
                        x: 10
                        y: 3
                        text: display
                        font.pointSize: 10
                    }
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            applicationListView.currentIndex = index;
                        }
                    }
                }
            }

            ListView {
                id: applicationListView
                anchors.fill: parent
                anchors.margins: margin
                model: IvyBus.application_list
                delegate: applicationName
                highlight: Rectangle { color: "lightsteelblue"; radius: 5 }
                focus: true
                onCurrentItemChanged: {
                    IvyBus.update_bindings_list(currentIndex);
                }
            }
        }
    }

    ColumnLayout {
        Layout.fillHeight: true
        Layout.fillWidth: true

        Label {
            text: "Application bindings"
            font.pointSize: 11
        }

        Rectangle {
            Layout.fillHeight: true
            Layout.fillWidth: true
            color: "#fff"
            border.width: 2
            border.color: "#ccc"
            radius: 3

            ListView {
                id: bindingsListView
                model: IvyBus.binding_list
                anchors.fill: parent
                anchors.margins: margin
                delegate: Text {
                        text: display
                        width: bindingsListView.width
                        font.pointSize: 9
                        wrapMode: Text.WordWrap
                    }
            }
        }
    }
}

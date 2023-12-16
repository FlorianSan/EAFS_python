import QtQuick 2.3
import QtQuick.Controls 2.2
import QtQuick.Controls.Material 2.2
import QtQuick.Dialogs 1.2
import QtQuick.Layouts 1.3
import fr.enac.IvyBus 1.0
import fr.enac.AircraftModel 1.0
import "./fcu" as Fcu
import "./widgets" as Widgets

ApplicationWindow {
    visible: true
    property int margin: 2
    height: mainLayout.implicitHeight + 4 * margin
    minimumWidth: mainLayout.Layout.minimumWidth + 4 * margin
    minimumHeight: mainLayout.Layout.minimumHeight + 4 * margin + 24
    maximumWidth: minimumWidth
    title: qsTr("Ivy Simulator Control")

    Timer {
        id: timer
    }
    function delay(cb, delayTime) {
        timer.interval = delayTime;
        timer.repeat = false;
        timer.triggered.connect(cb);
        timer.start();
    }

    ColumnLayout {
        id: mainLayout
        anchors.fill: parent
        anchors.margins: margin
        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
        spacing: 10

        RowLayout {
            Layout.fillWidth: true

            Widgets.Clock {
                id: clock
            }

            Widgets.AircraftModelState {
                Layout.leftMargin: 30
                timerLabel: clock.timerLabel
            }
        }

        Widgets.IntruderModelState { 
        }

        Fcu.Fcu {
            anchors.margins: margin
        }

        ColumnLayout {
            anchors.margins: margin
            Layout.alignment: Qt.AlignLeft | Qt.AlignTop
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.minimumWidth: 500
            Layout.minimumHeight: 280

            TabBar {
                id: ivyBar
                width: parent.width
                contentWidth: parent.width
                TabButton {
                    text: qsTr("Ivy messages")
                }
                TabButton {
                    text: qsTr("Ivy bindings")
                }
            }

            StackLayout {
                anchors.margins: margin
                currentIndex: ivyBar.currentIndex
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                Widgets.IvyConsole { }
                Widgets.IvyBindings { }
            }
        }
    }

    footer: RowLayout {
        id: footerLayout
        anchors.left: parent.left

        Rectangle {
            Layout.minimumHeight: 20
            Layout.fillWidth: true
            color: 'grey'

            Label {
                Layout.leftMargin: 20

                id: statusLabel
                text: ""
                font.pixelSize: 14
                font.italic: true
                color: "white"
            }
        }
    }
}

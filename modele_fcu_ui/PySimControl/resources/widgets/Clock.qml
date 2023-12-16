import QtQuick 2.3
import QtQuick.Controls 2.2
import QtQuick.Dialogs 1.2
import QtQuick.Layouts 1.1
import fr.enac.IvyBus 1.0
import fr.enac.AircraftModel 1.0

ColumnLayout {
    Layout.fillWidth: true
    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
    property alias timerLabel: timerValue

    function incrementTimer() {
        var cVal = parseFloat(timerValue.text);
        var value = cVal + parseFloat(clockIntervalSlider.value);
        timerValue.text = value.toFixed(1);

        IvyBus.send_msg("Time t="+value.toString());
    }

    ColumnLayout {
        Layout.fillWidth: true
        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

        // play / pause / next step buttons
        RowLayout {
            id: ivySimControl
            Layout.alignment: Qt.AlignCenter | Qt.AlignTop
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 10

            Timer {
                id: clockTimer
                interval: (clockIntervalSlider.value / clockSpeedSlider.value)*1000
                running: false
                repeat: true
                onTriggered: { incrementTimer(); }
            }

            Button {
                implicitWidth: 48
                implicitHeight: 48
                id: resetTimer
                opacity: enabled ? 1.0 : 0.7
                contentItem: Image {
                    source: "./icons/ic_replay_black_48dp.png"
                    fillMode: Image.PreserveAspectFit
                }
                onClicked: {
                    timerValue.text = "0.0"
                }
            }

            Button {
                implicitWidth: 48
                implicitHeight: 48
                id: startPauseTimer
                opacity: enabled ? 1.0 : 0.7
                contentItem: Image {
                    source: clockTimer.running ? "./icons/ic_pause_black_48dp.png" : "./icons/ic_play_arrow_black_48dp.png"
                    fillMode: Image.PreserveAspectFit
                }
                onClicked: {
                    clockTimer.running = !clockTimer.running
                }
            }

            Button {
                id: stepTimer
                implicitWidth: 48
                implicitHeight: 48
                enabled: !clockTimer.running
                opacity: enabled ? 1.0 : 0.7
                contentItem: Image {
                    source: "./icons/ic_fast_forward_black_48dp.png"
                    fillMode: Image.PreserveAspectFit
                }
                onClicked: { incrementTimer(); }
            }

            Label {
                id: timerValue
                text: qsTr("0.0")
                font.bold: true
                font.pointSize: 14
            }
        }

        // speed / interval sliders
        ColumnLayout {
            Layout.alignment: Qt.AlignCenter | Qt.AlignMiddle
            Layout.fillWidth: true
            Layout.fillHeight: true

            RowLayout {
                Label {
                    id: "clockSpeedLabel"
                    text: "Speed: "
                    font.pointSize: 11
                }

                Slider {
                    id: "clockSpeedSlider"
                    to: 5
                    from: 1
                    stepSize: 1
                    live: true
                    value: 2
                }

                Label {
                    id: "clockSpeedValueLabel"
                    text: "x"+clockSpeedSlider.value
                    font.pointSize: 11
                }
            }

            RowLayout {
                Label {
                    id: "clockIntervalLabel"
                    text: "Interval: "
                    font.pointSize: 11
                }

                Slider {
                    id: "clockIntervalSlider"
                    to: 1.0
                    from: 0.1
                    stepSize: 0.1
                    live: true
                    value: 1.0
                }

                Label {
                    id: "clockIntervalValueLabel"
                    text: clockIntervalSlider.value.toFixed(1)+"s"
                    font.pointSize: 11
                }
            }

        }
    }

}
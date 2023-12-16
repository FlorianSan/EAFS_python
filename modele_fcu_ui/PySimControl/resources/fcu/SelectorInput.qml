// a component to display digital counter

import QtQuick 2.3
import QtQuick.Controls 2.2
import fr.enac.IvyBus 1.0

Rectangle {
    property alias input: indicatorInput
    property alias text: indicatorText.text
    property PushButton controlButton
    property string ivyMessage
    property bool ivyAppendValue: true
    property alias validator: indicatorInput.validator
    property alias value: indicatorInput.text
    width: 76
    height: 47
    color: "#10101F"

    Text {
        id: indicatorText
        color: "#ffffff"
        font.pixelSize: 12
    }

    Rectangle {
        id: indicatorRect
        x: 8
        y: 15
        width: 67
        height: 31
        color: "#000000"
        border.color: !controlButton.managed ? "#ccc" : (indicatorInput.activeFocus ? "#f00" : "#001dff")
        border.width: 2

        TextInput {
            id: indicatorInput
            enabled: controlButton.managed
            width: 60
            height: 31
            y: 3
            x: 7
            color: "#02eb02"
            text:  "----"
            cursorVisible: false
            font.pixelSize: 20
            onFocusChanged: { }
            Keys.onReturnPressed: {
                var msg = ivyMessage;
                if (ivyAppendValue) {
                    msg += text;
                }
                IvyBus.send_msg(msg);
            }
        }
    }
}

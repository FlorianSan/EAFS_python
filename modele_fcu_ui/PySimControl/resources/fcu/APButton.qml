
import QtQuick 2.3
import QtQuick.Controls 2.2

Button {
    property bool activated: false

    width: 36
    height: 38
    text: ""
    opacity: activated ? 0.7 : 0.3
    background: Rectangle {
        implicitWidth: 34
        implicitHeight: 34
        border.width: 1
        border.color: "gray"
        radius: 5
        gradient: Gradient {
            GradientStop { position: 0 ; color: "gray" }
            GradientStop { position: 1 ; color: "green" }
        }
    }
}
// A styled rounded button to activate managed mode

import QtQuick 2.3
import QtQuick.Controls 2.2
import fr.enac.IvyBus 1.0


Button {
    property bool activated: false
    width: 34
    height: 34
    text: ""
    opacity: activated ? 0.9 : 0.5
    background: Rectangle {
        implicitWidth: 34
        implicitHeight: 34
        border.width: 1
        border.color: "gray"
        radius: 17
        gradient: Gradient {
            GradientStop { position: 0 ; color: "gray" }
            GradientStop { position: 1 ; color: "green" }
        }
    }
    onClicked: {
        activated = !activated;
    }
}
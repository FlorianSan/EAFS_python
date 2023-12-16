// A styled rounded button to activate managed mode

import QtQuick 2.3
import QtQuick.Controls 2.2
import fr.enac.IvyBus 1.0


Button {
    property bool managed: false
    property TextInput input
    property string ivyMessage
    width: 66
    height: 66
    text: ""
    opacity: managed ? 0.0 : 0.6
    background: Rectangle {
        implicitWidth: 70
        implicitHeight: 70
        border.width: 1
        border.color: "#888"
        radius: 35
        gradient: Gradient {
            GradientStop { position: 0 ; color: "#eee" }
            GradientStop { position: 1 ; color: "#ccc" }
        }
    }
    onClicked: {
        managed = !managed;
        if (!managed) {
            input.text = "----";
            IvyBus.send_msg(ivyMessage);
        } else {
            input.text = "";
            input.focus = true;
        }
    }
}
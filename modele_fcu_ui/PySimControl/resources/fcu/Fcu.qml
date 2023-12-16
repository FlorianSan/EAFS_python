import QtQuick 2.0
import QtQuick.Controls 2.2
import QtQuick.Dialogs 1.1
import QtQuick.Layouts 1.1
import fr.enac.IvyBus 1.0
import fr.enac.AP1 1.0

Rectangle {
    visible: true
    width: 638
    height: 216

    function generateVerticalMessage() {
        var msg = "FCUVertical Altitude="+altSelector.value+" Mode=";
        if (!vsManagedToggle.managed) {
            msg += "Selected Val=0";
        } else {
            msg += latVSModeSwitch.activated ? "FPA" : "V/S";
            msg += " Val="+vsSelector.value;
        }
        return msg;
    }

    Rectangle {
        width: 638
        height: 216

        Image {
            anchors.fill: parent
            source: "fcu.png"
        }

        /*
         * Speed control
         */
        SelectorInput {
            id: speedSelector
            controlButton: spdManagedToggle
            text: spdModeSwitch.activated ? "MACH" : "SPD"
            ivyMessage: "FCUSpeedMach Mode=Selected"+(text == "SPD" ? "Speed" : "Mach")+" Val="
            validator: DoubleValidator{bottom: 0; top: 1000;}
            x: 52
            y: 13
        }
        PushButton {
            id: spdManagedToggle
            input: speedSelector.input
            ivyMessage: "FCUSpeedMach Mode=Managed Val=0"
            x: 56
            y: 88
        }
        SwitchButton {
            id: spdModeSwitch
            x:8
            y:75
        }

        /*
         * heading control
         */
        SelectorInput {
            id: headingSelector
            controlButton: headingManagedToggle
            text: latVSModeSwitch.activated ? "TRK" : "HDG"
            validator: IntValidator{bottom: 0; top: 360;}
            ivyMessage: "FCULateral Mode=Selected"+(text == "HDG" ? "Heading" : "Track")+" Val="
            x: 150
            y: 13
        }
        PushButton {
            id: headingManagedToggle
            input: headingSelector.input
            ivyMessage: "FCULateral Mode=Managed Val=0"
            x: 162
            y: 88
        }
        SwitchButton {
            id: latVSModeSwitch
            x:303
            y:75
        }

        Rectangle {
            id: latLabelBackground
            x: 284
            y: 24
            width: 32
            height: 22
            color: "#10101F"
            border.width: 0

            Text {
                id: latLabel
                color: "#ffffff"
                font.pixelSize: 12
                text: latVSModeSwitch.activated ? "TRK" : "HDG"
            }
        }

        /*
         * Level control
         */
        Rectangle {
            id: vsLabelBackground
            x: 325
            y: 24
            width: 32
            height: 22
            color: "#10101F"
            border.width: 0

            Text {
                id: vsLabel
                color: "#ffffff"
                font.pixelSize: 12
                text: latVSModeSwitch.activated ? "FPA" : "V/S"
            }
        }
        SelectorInput {
            id: altSelector
            controlButton: altManagedToggle
            text: "ALT"
            validator: IntValidator{bottom: 0; top: 10000;}
            ivyMessage: generateVerticalMessage()
            ivyAppendValue: false
            x: 380
            y: 13
        }
        PushButton {
            id: altManagedToggle
            input: altSelector.input
            ivyMessage: "FCUVertical Altitude=0 Mode=Managed Val=0"
            x: 398
            y: 88
            onClicked: {
                if (!managed) {
                    // disable also vertical speed area
                    vsSelector.input.text = "----";
                    vsManagedToggle.managed = false;
                }
            }
        }

        /*
         * Vertical speed control
         */
        SelectorInput {
            id: vsSelector
            controlButton: vsManagedToggle
            text: latVSModeSwitch.activated ? "FPA" : "V/S"
            validator: DoubleValidator{bottom: -5000; top: 5000;}
            ivyMessage: generateVerticalMessage()
            ivyAppendValue: false
            x: 500
            y: 13
        }
        PushButton {
            id: vsManagedToggle
            input: vsSelector.input
            ivyMessage: generateVerticalMessage()
            enabled: altManagedToggle.managed
            x: 530
            y: 85
        }

        /*
         * Auto pilot Button
         */
         APButton {
            id: ap1Button
            x: 274
            y: 117
            activated: AP1.activated
            onClicked: {
                IvyBus.send_msg("FCUAP1 push");
            }
         }

        /*
         * Auto Thrust Button : always activated
         */
         APButton {
            id: athButton
            x: 301
            y: 170
            activated: true
         }
    }
}

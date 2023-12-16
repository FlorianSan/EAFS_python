
import QtQuick 2.3
import QtQuick.Controls 2.2
import QtQuick.Controls.Material 2.2
import QtQuick.Dialogs 1.2
import QtQuick.Layouts 1.1
import fr.enac.IvyBus 1.0
import fr.enac.AircraftModel 1.0

GridLayout {
    id: aircraftLayout
    columns: 3
    Layout.fillWidth: true
    property Label timerLabel

    Label {
        font.bold: true
        font.pointSize: 10
        text: qsTr("Aircraft Model:")
    }

    Button {
        text: qsTr("Init")
        highlighted: true
        Material.accent: Material.Green
        enabled: AircraftModel.connected
        onClicked: {
            AircraftModel.initialize()
        }
    }

    Button {
        text: qsTr("Reset")
        highlighted: true
        Material.accent: Material.Red
        enabled: AircraftModel.connected
        onClicked: {
            AircraftModel.reset()
            timerLabel.text = "0.0"
        }
    }

    Label {
        font.bold: true
        font.pointSize: 10
        text: qsTr("Status")
    }

    Label {
        Layout.columnSpan: 2
        font.pointSize: 10
        text: AircraftModel.connected ? "Running" : "Not running"
    }

    Label {
        font.bold: true
        font.pointSize: 10
        text: qsTr("Position")
    }

    Label {
        Layout.columnSpan: 2
        font.pointSize: 10
        text: AircraftModel.position
    }

    Label {
        font.bold: true
        font.pointSize: 10
        text: qsTr("Cmd Vector")
    }

    Label {
        Layout.columnSpan: 2
        font.pointSize: 10
        text: AircraftModel.command_vector
    }

}

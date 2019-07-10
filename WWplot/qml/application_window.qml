import QtQuick.Controls 2.4
import QtQuick 2.13
import QtQuick.Window 2.0
import wwplot 1.0
import QtQuick.Controls.Material 2.12
import QtQuick.Layouts 1.11

Window {
    id: root
    title: qsTr("WWplot")
    visible: true
    property int margin: 12
    width: mainLayout.implicitWidth + 2 * margin
    height: mainLayout.implicitHeight + 2 * margin
    minimumWidth: mainLayout.Layout.minimumWidth + 2 * margin
    minimumHeight: mainLayout.Layout.minimumHeight + 2 * margin
    Material.theme: Material.Dark
    Material.accent: Material.Purple

    ColumnLayout{
        id: mainLayout
        anchors.fill: parent
        anchors.margins: margin

        Pane {
            id: pane
            Layout.fillWidth: true
            Layout.fillHeight: true
            implicitWidth: 640
            implicitHeight: 480
            Layout.margins: margin
            Material.background: Material.Teal
            Material.elevation: 6

            ColumnLayout{
                spacing: 2
                anchors.fill: parent

                TableView {
                    id: table
                    model: TableModel {}
                    rowSpacing: 1
                    columnSpacing: 1
                    clip: true
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Layout.margins: 5
                    ScrollBar.horizontal: ScrollBar {}
                    ScrollBar.vertical: ScrollBar {}

                    delegate: Rectangle {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        implicitWidth: 100
                        implicitHeight: 25
                        border.color: "black"
                        border.width: 1

                        TextInput {
                            id: cellText
                            inputMethodHints: Qt.ImhDigitsOnly
                            text: display
                        }
                    }            
                }
            }
        }
    }
}
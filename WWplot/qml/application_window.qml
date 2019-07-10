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
            implicitWidth: paneLayout.Layout.minimumWidth + 2 * margin
            implicitHeight: paneLayout.Layout.minimumHeight + 2 * margin
            Layout.margins: margin
            Material.background: Material.Grey
            Material.elevation: 2

            ColumnLayout{
                id: paneLayout
                spacing: 2
                anchors.fill: parent

                TableView {
                    id: table
                    property int cellW: 100
                    property int cellH: 25
                    Layout.margins: 5
                    implicitWidth: 4 * cellW + 2 * Layout.margins
                    implicitHeight: 5 * cellH
                    model: TableModel {}
                    rowSpacing: 1
                    columnSpacing: 1
                    clip: true                    
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
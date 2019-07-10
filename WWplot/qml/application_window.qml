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
    width: 640
    height: 480
    Material.theme: Material.Dark
    Material.accent: Material.Purple

    RowLayout{
        anchors.fill: parent

        TableView {
            model: TableModel {}
            rowSpacing: 5
            columnSpacing: 5
            Layout.fillWidth: true
            Layout.fillHeight: true
            ScrollBar.horizontal: ScrollBar {}
            ScrollBar.vertical: ScrollBar {}

            delegate: Rectangle {
                    implicitWidth: root.width / 4
                    implicitHeight: 25
                    border.color: "black"
                    border.width: 1

                    TextInput {
                        id: cellText
                        inputMethodHints: Qt.ImhDigitsOnly
                        clip: true
                        width: parent.width
                        text: display
                    }
            }            
        }
    }
}
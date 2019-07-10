import QtQuick.Controls 2.4
import QtQuick 2.13
import QtQuick.Window 2.0
import wwplot 1.0

Window {
    id: root
    title: qsTr("WWplot")
    visible: true
    width: 640
    height: 480

    TableView {
        anchors.fill: parent
        columnSpacing: 1
        rowSpacing: 1

        model: TableModel {}

        delegate: Rectangle {
            implicitWidth: 100
            implicitHeight: 50

            Rectangle {
                id: bar
                
                width: parent.width * display / 100.0
                height: 30
                color: "green"
            }

            TextInput {
                inputMethodHints: Qt.ImhDigitsOnly

                anchors.verticalCenter: parent.verticalCenter
                anchors.right: parent.right

                width: parent.width * 0.70
                height: parent.height * 0.6
                
                text: display
            }   
        }
    }
}
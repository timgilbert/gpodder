
import Qt 4.7

import 'config.js' as Config
import 'util.js' as Util

Item {
    id: root

    property real progress: 0
    property int duration: 0
    property real mousepos: 0
    signal setProgress(real progress)

    height: 64 * Config.scale

    BorderImage {
        anchors {
            verticalCenter: parent.verticalCenter
            left: parent.left
            right: parent.right
        }

        height: 9

        source: 'artwork/slider-bg.png'

        Rectangle {
            id: seekTimePreviewBackground

            anchors.fill: seekTimePreview
            color: 'black'
            opacity: seekTimePreview.opacity*.8
            radius: Config.largeSpacing
            smooth: true
        }

        Text {
            id: seekTimePreview
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.bottom: parent.top
            anchors.bottomMargin: Config.largeSpacing * 7
            text: ' ' + Util.formatDuration(root.mousepos*duration) + ' '
            font.pixelSize: 50 * Config.scale
            horizontalAlignment: Text.AlignHCenter
            color: 'white'
            opacity: mouseArea.pressed?1:0
            scale: mouseArea.pressed?1:.5
            transformOrigin: Item.Bottom

            Behavior on opacity { PropertyAnimation { } }
            Behavior on scale { PropertyAnimation { } }
        }

        border {
            top: 2
            left: 2
            right: 2
            bottom: 2
        }

        BorderImage {
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.leftMargin: parent.border.left
            anchors.topMargin: parent.border.top

            width: Math.max(1, (parent.width-parent.border.left-parent.border.right) * root.progress)
            source: 'artwork/slider-fg.png'
            clip: true

            Image {
                source: 'artwork/slider-dot.png'
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: parent.right
                anchors.leftMargin: -width
            }
        }

    }
    MouseArea {
        id: mouseArea

        anchors.fill: parent
        onClicked: {
            root.setProgress(mouse.x / root.width)
        }
        onPositionChanged: {
            root.mousepos = (mouse.x/root.width)
            if (root.mousepos < 0) root.mousepos = 0
            if (root.mousepos > 1) root.mousepos = 1
        }
        onPressed: {
            root.mousepos = (mouse.x/root.width)
            if (root.mousepos < 0) root.mousepos = 0
            if (root.mousepos > 1) root.mousepos = 1
        }
    }
}


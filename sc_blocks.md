# Block ids

## Math
| Selector              | Block                                                                                           |
|-----------------------|-------------------------------------------------------------------------------------------------|
| `+`                   | () + ()                                                                                         |
| `-`                   | () - ()                                                                                         |
| `*`                   | () * ()                                                                                         |
| `/`                   | () / ()                                                                                         |
| `%`                   | () % ()                                                                                         |
| `rounded`             | Round ()                                                                                        |
| `computeFunction:of:` | () of () ([Other math functions](https://en.scratch-wiki.info/wiki/()_of_()_(Operators_block))) |

## Logic
| Selector            | Block     |
|---------------------|-----------|
| `&`                 | () and () |
| <code>&#124;</code> | () or ()  |
| `not`               | not ()    |
| `<`                 | () < ()   |
| `=`                 | () == ()  |
| `>`                 | () > ()   |

## Variables / Lists
### Variables
| Selector        | Block               |
|-----------------|---------------------|
| `readVariable`  | () (Variable block) |
| `setVar:to:`    | Set () to ()        |
| `showVariable:` | Show Variable ()    |
| `hideVariable:` | Hide Variable ()    |

### Lists
| Selector             | Block                         |
|----------------------|-------------------------------|
| `contentsOfList:`    | () (List block)               |
| `getLine:ofList:`    | Item () of ()                 |
| `lineCountOfList:`   | Length of () (List block)     |
| `list:contains:`     | () Contains ()                |
| `setLine:ofList:to:` | Replace Item () of () with () |
| `append:toList:`     | Add () to ()                  |
| `insert:at:ofList:`  | Insert () at () of ()         |
| `deleteLine:ofList:` | Delete () of ()               |
| `showList:`          | Show List ()                  |
| `hideList:`          | Hide List ()                  |

## Flow control / C Blocks (or whatever it's called)
| Selector    | Block            |
|-------------|------------------|
| `doIf`      | If () Then       |
| `doIfElse`  | If () Then, Else |
| `doRepeat`  | Repeat ()        |
| `doUntil`   | Repeat Until ()  |
| `doForever` | Forever          |


## Other
| Selector                        | Block                          |
|---------------------------------|--------------------------------|
| `answer`                        | Answer                         |
| `backgroundIndex`               | Backdrop #                     |
| `bounceOffEdge`                 | If on Edge, Bounce             |
| `broadcast:`                    | Broadcast ()                   |
| `changeGraphicEffect:by:`       | Change () Effect by ()         |
| `changePenHueBy:`               | Change Pen Color by ()         |
| `changePenShadeBy:`             | Change Pen Shade by ()         |
| `changePenSizeBy:`              | Change Pen Size by ()          |
| `changeSizeBy:`                 | Change Size by ()              |
| `changeTempoBy:`                | Change Tempo by ()             |
| `changeVar:by:`                 | Change () by ()                |
| `changeVolumeBy:`               | Change Volume by ()            |
| `changeXposBy:`                 | Change X by ()                 |
| `changeYposBy:`                 | Change Y by ()                 |
| `clearPenTrails`                | Clear                          |
| `CLR_COUNT`                     | Clear Counter                  |
| `color:sees:`                   | Color () is Touching ()?       |
| `comeToFront`                   | Go to Front                    |
| `concatenate:with:`             | Join ()()                      |
| `costumeIndex`                  | Costume #                      |
| `costumeName`                   | Costume Name                   |
| `COUNT`                         | Counter                        |
| `createCloneOf`                 | Create Clone of ()             |
| `deleteClone`                   | Delete This Clone              |
| `distanceTo:`                   | Distance to ()                 |
| `doAsk`                         | Ask () and Wait                |
| `doBroadcastAndWait`            | Broadcast () and Wait          |
| `doPlaySoundAndWait`            | Play Sound () Until Done       |
| `doReturn`                      | Stop Script                    |
| `doWaitUntil`                   | Wait Until ()                  |
| `drum:duration:elapsed:from:`   | Play Drum () for () Beats      |
| `filterReset`                   | Clear Graphic Effects          |
| `forward:`                      | Move () Steps                  |
| `fxTest`                        | Color FX Test ()               |
| `getAttribute:of:`              | () of () (Sensing block)       |
| `getParam`                      | custom block parameter         |
| `getUserId`                     | User ID                        |
| `getUserName`                   | Username                       |
| `glideSecs:toX:y:elapsed:from:` | Glide () Secs to X: () Y: ()   |
| `goBackByLayers:`               | Go Back () Layers              |
| `gotoSpriteOrMouse:`            | Go to ()                       |
| `gotoX:y:`                      | Go to X: () Y: ()              |
| `heading`                       | Direction                      |
| `heading:`                      | Point in Direction ()          |
| `hide`                          | Hide                           |
| `hideAll`                       | Hide All Sprites               |
| `INCR_COUNT`                    | Increment Counter              |
| `instrument:`                   | Set Instrument to ()           |
| `isLoud`                        | Loud?                          |
| `keyPressed:`                   | Key () Pressed?                |
| `letter:of:`                    | Letter () of ()                |
| `lookLike:`                     | Switch Costume to ()           |
| `midiInstrument:`               | Set Instrument to ()           |
| `mousePressed`                  | Mouse Down?                    |
| `mouseX`                        | Mouse X                        |
| `mouseY`                        | Mouse Y                        |
| `nextCostume`                   | Next Costume                   |
| `nextScene`                     | Next Backdrop                  |
| `noteOn:duration:elapsed:from:` | Play Note () for () Beats      |
| `obsolete`                      | Obsolete                       |
| `penColor:`                     | Set Pen Color to ()            |
| `penSize:`                      | Set Pen Size to ()             |
| `playDrum`                      | Play Drum () for () Beats      |
| `playSound:`                    | Play Sound ()                  |
| `pointTowards:`                 | Point Towards ()               |
| `putPenDown`                    | Pen Down                       |
| `putPenUp`                      | Pen Up                         |
| `randomFrom:to:`                | Pick Random () to ()           |
| `rest:elapsed:from:`            | Rest for () Beats              |
| `say:`                          | Say ()                         |
| `say:duration:elapsed:from:`    | Say () for () Seconds          |
| `sayNothing`                    | Say Nothing                    |
| `scale`                         | Size                           |
| `sceneName`                     | Backdrop Name                  |
| `scrollAlign`                   | Align Scene ()                 |
| `scrollRight`                   | Scroll Right ()                |
| `scrollUp`                      | Scroll Up ()                   |
| `senseVideoMotion`              | Video () on ()                 |
| `sensor:`                       | () Sensor Value                |
| `sensorPressed:`                | Sensor ()?                     |
| `setGraphicEffect:to:`          | Set () Effect to ()            |
| `setPenHueTo:`                  | Set Pen Color to ()            |
| `setPenShadeTo:`                | Set Pen Shade to ()            |
| `setRotationStyle`              | Set Rotation Style ()          |
| `setSizeTo:`                    | Set Size to ()%                |
| `setTempoTo:`                   | Set Tempo to () bpm            |
| `setVideoState`                 | Turn Video ()                  |
| `setVideoTransparency`          | Set Video Transparency to ()%  |
| `setVolumeTo:`                  | Set Volume to ()%              |
| `show`                          | Show                           |
| `soundLevel`                    | Loudness                       |
| `stampCostume`                  | Stamp                          |
| `startScene`                    | Switch Backdrop to ()          |
| `startSceneAndWait`             | Switch Backdrop to () and Wait |
| `stopAll`                       | Stop All                       |
| `stopAllSounds`                 | Stop All Sounds                |
| `stopScripts`                   | Stop ()                        |
| `stopSound:`                    | Stop Sound ()                  |
| `stringLength:`                 | Length of () (Operators block) |
| `tempo`                         | Tempo                          |
| `think:`                        | Think ()                       |
| `think:duration:elapsed:from:`  | Think () for () Seconds        |
| `timeAndDate`                   | Current ()                     |
| `timer`                         | Timer                          |
| `timerReset`                    | Reset Timer                    |
| `timestamp`                     | Days Since 2000                |
| `touching:`                     | Touching ()?                   |
| `touchingColor:`                | Touching Color ()?             |
| `turnAwayFromEdge`              | Point Away From Edge           |
| `turnLeft:`                     | Turn () Degrees                |
| `turnRight:`                    | Turn () Degrees                |
| `undefined`                     | Undefined                      |
| `volume`                        | Volume                         |
| `wait:elapsed:from:`            | Wait () Seconds                |
| `warpSpeed`                     | All at Once                    |
| `whenClicked`                   | When This Sprite Clicked       |
| `whenCloned`                    | When I Start as a Clone        |
| `whenGreenFlag`                 | When Green Flag Clicked        |
| `whenIReceive`                  | When I Receive ()              |
| `whenKeyPressed`                | When () Key Pressed            |
| `whenSceneStarts`               | When Backdrop Switches to ()   |
| `whenSensorGreaterThan`         | When () is greater than ()     |
| `xpos`                          | X Position                     |
| `xpos:`                         | Set X to ()                    |
| `xScroll`                       | X Scroll                       |
| `ypos`                          | Y Position                     |
| `ypos:`                         | Set Y to ()                    |
| `yScroll`                       | Y Scroll                       |


## Experimental / Hidden
| Selector    | Block             |
|-------------|-------------------|
| `doForLoop` | For Each () in () |
| `doWhile`   | While ()          |



## Obsolete / removed
| Selector      | Block                               |
|---------------|-------------------------------------|
| `doForeverIf` | Forever If ()                       |
| `abs`         | Abs () (Use `computeFunction:of:`)  |
| `sqrt`        | Sqrt () (Use `computeFunction:of:`) |


HELP_TEXT = (
    "Use Telegram menu commands with /.\n"
    "Send ASF commands with !.\n"
    "Examples:\n"
    "!status\n"
    "!2fa <bot>\n"
    "!redeem <bot> <key>"
)

ASF_COMMANDS_TEXT = """Telegram commands:
/help - Show wrapper usage
/commands - List ASF command names

ASF commands use ! prefix in Telegram:
!status
!redeem <bot> <key>

ASF command list:
2fa [Bots]
2fafinalize [Bots] <ActivationCode>
2fafinalized [Bots] <2FACodeFromApp>
2fafinalizedforce [Bots]
2fainit [Bots]
2fano [Bots]
2faok [Bots]
addlicense [Bots] <Licenses>
balance [Bots]
bgr [Bots]
bgrclear [Bots]
encrypt <encryptionMethod> <stringToEncrypt>
exit
farm [Bots]
fb [Bots]
fbadd [Bots] <AppIDs>
fbrm [Bots] <AppIDs>
fq [Bots]
fqadd [Bots] <AppIDs>
fqrm [Bots]
hash <hashingMethod> <stringToHash>
help
input [Bots] <Type> <Value>
inventory [Bots]
level [Bots]
loot [Bots]
loot@ [Bots] <AppIDs>
loot% [Bots] <AppIDs>
loot^ [Bots] <AppID> <ContextID>
loot& [Bots] <AppID> <ContextID> <Rarities>
mab [Bots]
mabadd [Bots] <AppIDs>
mabrm [Bots]
match [Bots]
nickname [Bots] <Nickname>
owns [Bots] <Games>
pause [Bots]
pause~ [Bots]
pause& [Bots] <Seconds>
play [Bots] <AppIDs,GameName>
points [Bots]
privacy [Bots] <Settings>
redeem [Bots] <Keys>
redeem^ [Bots] <Modes> <Keys>
redeempoints [Bots] <DefinitionIDs>
reset [Bots]
restart
resume [Bots]
rmlicense [Bots] <Licenses>
start [Bots]
stats
status [Bots]
std [Bots]
stop [Bots]
tb [Bots]
tbadd [Bots] <SteamIDs64>
tbrm [Bots]
transfer [Bots] <TargetBot>
transfer@ [Bots] <AppIDs> <TargetBot>
transfer% [Bots] <AppIDs> <TargetBot>
transfer^ [Bots] <AppID> <ContextID> <TargetBot>
transfer& [Bots] <AppID> <ContextID> <TargetBot> <Rarities>
unpack [Bots]
update [Channel]
updateplugins [Channel] [Plugins]
version"""

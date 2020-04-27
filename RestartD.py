# coding: utf8
import time

# 0=guest, 1=user, 2=helper, 3=admin
permissionLevel = 2
permissionLevelAbort = 1

abort = False
running = False

HelpMessage = '''------MCDR Quick Reboot------
一个简易的服务器可控快速重启插件
使用方法：
!!restart start 启动重启服务器的10秒倒计时，需要服务器助理权限
!!restart abort 中止服务器重启操作，需要服务器用户权限'''

def restart_d_restart(server, info):
    global abort
    global running
    running = True
    server.reply(info, '服务器将在10秒后重启')
    server.reply(info, '输入!!restart abort来中止重启')
    t = 9
    while True:
        if abort:
            running = False
            abort = False
            return

        time.sleep(1)
        server.reply(info, '服务器将在' + str(t) + '秒后重启')
        t -= 1

        if (t == 1):
            time.sleep(1)
            server.logger.info('Server stopping')
            server.stop()
            while True:
                if not server.is_server_running():
                    break            
            server.logger.info('Server starting')
            server.start()
            running = False
            return

def restart_d_abort(server, info):
    server.reply(info, '重启操作已中止！')
    global abort
    abort = True

def on_info(server, info):
    if info.content == '!!restart start' and info.is_player:
        if server.get_permission_level(info.player) >= permissionLevel:
            restart_d_restart(server, info)
        else:
            server.tell(info.player, '权限不足！')

    if info.content == '!!restart':
        if info.is_player:
            server.tell(info.player, HelpMessage)
        elif not info.is_player and info.source == 1:
            server.logger.info("\n" + HelpMessage)

    elif not info.is_player and info.source == 1:
        if info.content == '!!restart start':
            restart_d_restart(server, info)
        elif info.content == '!!restart abort':
            if running:
                restart_d_abort(server, info)
            else:
                server.logger.info('重启操作未运行')

    elif info.content == '!!restart abort' and info.is_player:
        if running:
            if server.get_permission_level(info.player) >= permissionLevelAbort:
                restart_d_abort(server, info)
            else:
                server.tell(info.player, '权限不足！')
        else:
            server.tell(info.player, '重启操作未运行')

def on_unload(server):
    if running:
        global abort
        abort = True

def on_mcdr_stop(server):
    if running:
        global abort
        abort = True

def on_load(server, old_module):
    server.add_help_message('!!restart', '快速、可控地重启服务器')
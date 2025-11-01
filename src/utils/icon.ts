import { addCollection } from '@iconify/vue';

import qlementine from '@iconify/json/json/qlementine-icons.json'
import oui from '@iconify/json/json/oui.json'
import eos from '@iconify/json/json/eos-icons.json'
import noto from '@iconify/json/json/nimbus.json'
import uil from '@iconify/json/json/uil.json'
import vscode from '@iconify/json/json/vscode-icons.json'
import catppuccin from '@iconify/json/json/catppuccin.json'
import ic from '@iconify/json/json/ic.json'

addCollection({
  prefix: 'i',
  icons: {
    script: qlementine.icons['file-script-16'],
    scripts: oui.icons['app-console'],
    task: qlementine.icons['task-16'],
    refresh: qlementine.icons['refresh-16'],
    content: qlementine.icons['file-text-16'],
    devtool: oui.icons['app-devtools'],
    search: qlementine.icons['search-16'],
    run: oui.icons['index-runtime'],
    home: oui.icons['home'],
    setting: qlementine.icons['settings-16'],
    open: qlementine.icons['folder-open-16'],
    interface: oui.icons['vis-tag-cloud'],
    fire: noto.icons['fire'],
    winpowershell: catppuccin.icons['powershell'],
    powershell: catppuccin.icons['powershell'],
    document: oui.icons['document'],
  },
  width: 16,
  height: 16,
});

addCollection({
  prefix: 'i',
  icons: {
    running: eos.icons['loading'],
    calender: uil.icons['calender'],
    setting: uil.icons['setting'],
    calculate: ic.icons['outline-calculate'],
  },
  width: 24,
  height: 24,
});

addCollection({
  prefix: 'i',
  icons: {
    python: vscode.icons['file-type-python'],
  },
  width: 32,
  height: 32,
});

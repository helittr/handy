export interface devInfoItem {
  label: string
  value: string
}

export interface dev {
  basicInfo: {
    label: string
    serial: devInfoItem
    model: devInfoItem
    project: devInfoItem
    more: devInfoItem[]
  }
  otherInfo: {
    label: string
    more: devInfoItem[]
  }[]
}

export interface quickBtn {
  label: string
  type: string
  icon?: string
}

export function get_devs(): dev[] {
  return [
    {
      basicInfo: {
        label: '基本信息',
        serial: { label: '序列号', value: '1234567890' },
        model: { label: '型号', value: 'Pixel 6 Pro' },
        project: { label: '项目', value: 'Android 12' },
        more: [
          { label: 'Android版本', value: '12.0.0' },
          { label: '内核版本', value: '4.14.232' },
          { label: '安全补丁级别', value: '2023-10-01' },
        ],
      },
      otherInfo: [
        {
          label: '其他信息',
          more: [
            { label: 'IMEI', value: '123456789012345' },
            { label: 'Wi-Fi MAC地址', value: '00:11:22:33:44:55' },
            { label: '蓝牙MAC地址', value: '66:77:88:99:A0:B1' },
          ],
        },
      ],
    },
    {
      basicInfo: {
        label: '基本信息',
        serial: { label: '序列号', value: '0987654321' },
        model: { label: '型号', value: 'Pixel 5' },
        project: { label: '项目', value: 'Android 11' },
        more: [
          { label: 'Android版本', value: '11.0.0' },
          { label: '内核版本', value: '4.14.232' },
          { label: '安全补丁级别', value: '2023-10-01' },
        ],
      },
      otherInfo: [
        {
          label: '其他信息',
          more: [
            { label: 'IMEI', value: '543216789012345' },
            { label: 'Wi-Fi MAC地址', value: '55:44:33:22:11:00' },
            { label: '蓝牙MAC地址', value: 'B1:A0:99:88:77:66' },
          ],
        },
      ],
    },
  ]
}

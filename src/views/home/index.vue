<template>
  <div class="home">

    <n-popover placement="left-start" trigger="click" :width="500" scrollable>
      <template #trigger>
        <n-button class="btn" circle @click="onClick">
          <template #icon>
            <Icon class="icon" icon="i:setting" />
          </template>
        </n-button>
      </template>

      <n-form class="control-panel" label-placement="left" size="small">
        <n-form-item label="数量：">
          <n-slider v-model:value="param.maxCircleNumber" :min="1" :max="1000" size="tiny" />
          <n-input-number v-model:value="param.maxCircleNumber" :min="1" :max="1000" size="tiny" />
        </n-form-item>
        <n-form-item label="重力：">
          <n-slider v-model:value="param.gravity" :min="0" :max="0.9" :step="0.01" size="tiny" />
          <n-input-number v-model:value="param.gravity" :min="0" :max="0.9" :step="0.01" size="tiny" />
        </n-form-item>
        <n-form-item label="弹跳：">
          <n-slider v-model:value="param.bounce" :min="0" :max="0.9" :step="0.01" size="tiny" />
          <n-input-number v-model:value="param.bounce" :min="0" :max="0.9" :step="0.01" size="tiny" />
        </n-form-item>
      </n-form>

    </n-popover>

    <div class="clock-canvas" ref="clockCanvasContainer">
      <canvas ref="clockCanvas"></canvas>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, type Ref, reactive } from 'vue'

import { NButton, NPopover, NForm, NFormItem, NSlider, NInputNumber } from 'naive-ui'
import { Icon } from '@iconify/vue'

const dialogVisible = ref(false)

function onClick() {
  // Handle button click
  console.log('Button clicked')
  dialogVisible.value = true
}

const clockCanvas = ref<HTMLCanvasElement | null>(null)
const clockCanvasContainer = ref<HTMLDivElement | null>(null)
let animationFrameId: number
const circleSize = ref(8)

const param = reactive({
  gravity: 0.1, // Default gravity value
  maxCircleNumber: 100, // Default maximum number of circles
  bounce: 0.8 // Default bounce factor
})

interface Circle {
  x: number
  y: number
  radius: number
  color: string
  vx: number
  vy: number
  gravity: number
  bounce: number
}

const digitCircles: Circle[][] = Array(8).fill(null).map(() => []) // Current display circles
const newDigitCircles: Circle[][] = Array(8).fill(null).map(() => []) // New circles being created
const fallingCircles = ref<Circle[]>([]) as Ref<Circle[]> // Explicit type declaration
let currentTime = ''
let prevTime = ''

function drawClock() {
  if (!clockCanvas.value) return

  const ctx = clockCanvas.value.getContext('2d')
  if (!ctx) return

  const now = new Date()
  const timeStr = now.getHours().toString().padStart(2, '0') + ':' +
    now.getMinutes().toString().padStart(2, '0') + ':' +
    now.getSeconds().toString().padStart(2, '0')

  if (timeStr !== currentTime) {
    if (currentTime) {
      // Save previous time before updating
      prevTime = currentTime
      // Trigger falling animation only for changed digits
      const changedPositions: number[] = []
      for (let i = 0; i < Math.min(prevTime.length, currentTime.length); i++) {
        if (prevTime[i] !== ':' && currentTime[i] !== ':' && prevTime[i] !== currentTime[i]) {
          changedPositions.push(i)
        }
      }
      animateFall(changedPositions)
    }
    currentTime = timeStr
    createNumberCircles(timeStr)
  }

  ctx.clearRect(0, 0, clockCanvas.value.width, clockCanvas.value.height)

  // Draw all digit circles
  digitCircles.forEach(digit => {
    digit.forEach(circle => {
      ctx.beginPath()
      ctx.arc(circle.x, circle.y, circle.radius, 0, Math.PI * 2)
      ctx.fillStyle = circle.color
      ctx.fill()
    })
  })

  // Draw falling circles
  fallingCircles.value.forEach(circle => {
    ctx.beginPath()
    ctx.arc(circle.x, circle.y, circle.radius, 0, Math.PI * 2)
    ctx.fillStyle = circle.color
    ctx.fill()
  })

  animationFrameId = requestAnimationFrame(drawClock)
}

function getDigitPattern(digit: number): number[][] {
  // 7x5 patterns for digits 0-9
  const patterns = [
    // 0
    [
      [1, 1, 1, 1, 1],
      [1, 0, 0, 0, 1],
      [1, 0, 0, 0, 1],
      [1, 0, 0, 0, 1],
      [1, 0, 0, 0, 1],
      [1, 0, 0, 0, 1],
      [1, 1, 1, 1, 1]
    ],
    // 1
    [
      [0, 0, 1, 0, 0],
      [0, 1, 1, 0, 0],
      [0, 0, 1, 0, 0],
      [0, 0, 1, 0, 0],
      [0, 0, 1, 0, 0],
      [0, 0, 1, 0, 0],
      [0, 1, 1, 1, 0]
    ],
    // 2
    [
      [1, 1, 1, 1, 1],
      [0, 0, 0, 0, 1],
      [0, 0, 0, 0, 1],
      [1, 1, 1, 1, 1],
      [1, 0, 0, 0, 0],
      [1, 0, 0, 0, 0],
      [1, 1, 1, 1, 1]
    ],
    // 3
    [
      [1, 1, 1, 1, 1],
      [0, 0, 0, 0, 1],
      [0, 0, 0, 0, 1],
      [1, 1, 1, 1, 1],
      [0, 0, 0, 0, 1],
      [0, 0, 0, 0, 1],
      [1, 1, 1, 1, 1]
    ],
    // 4
    [
      [1, 0, 0, 0, 1],
      [1, 0, 0, 0, 1],
      [1, 0, 0, 0, 1],
      [1, 1, 1, 1, 1],
      [0, 0, 0, 0, 1],
      [0, 0, 0, 0, 1],
      [0, 0, 0, 0, 1]
    ],
    // 5
    [
      [1, 1, 1, 1, 1],
      [1, 0, 0, 0, 0],
      [1, 0, 0, 0, 0],
      [1, 1, 1, 1, 1],
      [0, 0, 0, 0, 1],
      [0, 0, 0, 0, 1],
      [1, 1, 1, 1, 1]
    ],
    // 6
    [
      [1, 1, 1, 1, 1],
      [1, 0, 0, 0, 0],
      [1, 0, 0, 0, 0],
      [1, 1, 1, 1, 1],
      [1, 0, 0, 0, 1],
      [1, 0, 0, 0, 1],
      [1, 1, 1, 1, 1]
    ],
    // 7
    [
      [1, 1, 1, 1, 1],
      [0, 0, 0, 0, 1],
      [0, 0, 0, 1, 0],
      [0, 0, 1, 0, 0],
      [0, 1, 0, 0, 0],
      [1, 0, 0, 0, 0],
      [1, 0, 0, 0, 0]
    ],
    // 8
    [
      [1, 1, 1, 1, 1],
      [1, 0, 0, 0, 1],
      [1, 0, 0, 0, 1],
      [1, 1, 1, 1, 1],
      [1, 0, 0, 0, 1],
      [1, 0, 0, 0, 1],
      [1, 1, 1, 1, 1]
    ],
    // 9
    [
      [1, 1, 1, 1, 1],
      [1, 0, 0, 0, 1],
      [1, 0, 0, 0, 1],
      [1, 1, 1, 1, 1],
      [0, 0, 0, 0, 1],
      [0, 0, 0, 0, 1],
      [1, 1, 1, 1, 1]
    ]
  ]
  return patterns[digit]
}

function createNumberCircles(timeStr: string, triggerAnimation = true) {
  // Find which digits changed
  const changedPositions: number[] = []
  if (triggerAnimation && prevTime) {
    for (let i = 0; i < Math.min(prevTime.length, timeStr.length); i++) {
      if (prevTime[i] !== ':' && timeStr[i] !== ':' && prevTime[i] !== timeStr[i]) {
        changedPositions.push(i)
      }
    }
  } else {
    // First run or no animation needed - update all digits
    for (let i = 0; i < timeStr.length; i++) {
      if (timeStr[i] !== ':') {
        changedPositions.push(i)
      }
    }
  }

  if (!clockCanvas.value) return

  const canvasWidth = clockCanvas.value.width
  const canvasHeight = clockCanvas.value.height

  // Calculate positions to fill canvas
  const digitWidth = canvasWidth / 8
  const digitHeight = canvasHeight / 2
  const digitPositions = [
    [digitWidth * 0.8, canvasHeight * 0.5],
    [digitWidth * 2.0, canvasHeight * 0.5],

    [digitWidth * 2.5, canvasHeight * 0.5],

    [digitWidth * 3.4, canvasHeight * 0.5],
    [digitWidth * 4.6, canvasHeight * 0.5],

    [digitWidth * 5.5, canvasHeight * 0.5],

    [digitWidth * 6.2, canvasHeight * 0.5],
    [digitWidth * 7.3, canvasHeight * 0.5]
  ]

  // Calculate circle size to fill digit height
  const newCircleSize = Math.min(digitHeight / 7, digitWidth / 5)
  circleSize.value = newCircleSize

  // Create new circles for all digits
  timeStr.split('').forEach((char, i) => {
    if (char === ':') return
    if (i >= newDigitCircles.length) return

    const digit = parseInt(char)
    const [x, y] = digitPositions[i]
    const digitPattern = getDigitPattern(digit)

    newDigitCircles[i] = [] // Clear existing new circles

    for (let row = 0; row < digitPattern.length; row++) {
      for (let col = 0; col < digitPattern[row].length; col++) {
        if (digitPattern[row][col]) {
          newDigitCircles[i].push({
            x: x + (col - 2) * circleSize.value,
            y: y + (row - 3) * circleSize.value,
            radius: circleSize.value / 2,
            color: `hsl(${Math.floor(Math.random() * 360)}, 65%, 50%)`,

            vy: -5 - Math.random() * 5,
            vx: (Math.random() - 0.5) * 10,
            gravity: param.gravity + (1 - param.gravity - 0.1) * Math.random(),
            bounce: param.bounce + (1 - param.bounce - 0.1) * Math.random()
          })
        }
      }
    }
  })

  // For changed digits, trigger animation
  if (changedPositions.length > 0) {
    animateFall(changedPositions)
  } else {
    // No changes, just update display
    digitCircles.splice(0, digitCircles.length, ...newDigitCircles.map(arr => [...arr]))
  }
}

let animationStarted = false

function animateFall(changedPositions: number[]) {
  // Create a copy of old circles for animation
  const oldCircles: Circle[][] = []
  changedPositions.forEach(pos => {
    oldCircles[pos] = [...digitCircles[pos]]
  })

  // Show new digits immediately
  changedPositions.forEach(pos => {
    digitCircles[pos] = [...newDigitCircles[pos]]
  })

  // Animate old digits falling
  while (fallingCircles.value.length > param.maxCircleNumber) {
    // Clear existing falling circles if any
    fallingCircles.value.shift()
  }
  changedPositions.forEach(pos => {
    oldCircles[pos].forEach(circle => {
      fallingCircles.value.push(circle)
    })
  })

  function update() {
    fallingCircles.value.forEach(circle => {
      circle.vy += circle.gravity
      circle.y += circle.vy
      circle.x += circle.vx

      if (circle.y + circle.radius > clockCanvas.value!.height) {
        circle.y = clockCanvas.value!.height - circle.radius
        circle.vy *= -circle.bounce
        circle.vx *= 0.9 // Slightly reduce horizontal speed on bounce
      }
    })

    requestAnimationFrame(update)
  }

  if (!animationStarted) {
    animationStarted = true
    requestAnimationFrame(update)
  }
}

function resizeCanvas() {
  if (!clockCanvas.value) return

  const container = clockCanvas.value.parentElement
  if (!container) return

  clockCanvas.value.width = container.clientWidth
  clockCanvas.value.height = container.clientHeight

  // Force recreate all numbers with new dimensions
  if (currentTime) {
    createNumberCircles(currentTime, false) // Resize without animation
  }
}

function debounce<T extends (...args: unknown[]) => void>(func: T, delay: number): (...args: Parameters<T>) => void {
  let timer: number
  return function (this: unknown, ...args: Parameters<T>) {
    clearTimeout(timer)
    timer = setTimeout(() => {
      func.apply(this, args)
    }, delay)
  }
}

const debouncedResize = debounce(resizeCanvas, 300)

onMounted(() => {
  if (clockCanvas.value) {
    resizeCanvas()
    drawClock()
    window.addEventListener('resize', debouncedResize)
  }
})

const ob: ResizeObserver = new ResizeObserver(() => {
  debouncedResize()
})

onMounted(() => {
  ob.observe(clockCanvasContainer.value!)
  clockCanvasContainer.value!.addEventListener('scroll', debouncedResize, { passive: true })
  // cancelAnimationFrame(animationFrameId)
})

onUnmounted(() => {
  ob.disconnect()
  cancelAnimationFrame(animationFrameId)
})
</script>

<style scoped>
.home {
  height: 100%;
  width: 100%;
  padding: 0;
  position: relative;
}

.control-panel {
  width: 100%;
}

.control-card {
  width: 100%;
}

.clock-canvas {
  width: 100%;
  height: 100%;
  padding: 0px;
  overflow: hidden;
}

.btn {
  position: absolute;
  top: 10px;
  left: calc(100% - 50px);
}
</style>

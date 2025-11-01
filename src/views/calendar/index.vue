<template>
  <n-calendar class="calendar"
  #="{ year, month, date }"
  >

  </n-calendar>
</template>

<script lang="ts" setup>
import { NCalendar } from 'naive-ui';

</script>

<style scoped>
.calendar {
  width: 100%;
  height: 100%;
  padding: 10px;
  box-sizing: border-box;
}

:deep(.n-calendar-cell--current) {
  background-color: var(--n-date-color-current);
}
</style>

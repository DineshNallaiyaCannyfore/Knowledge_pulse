<script setup lang="ts">
import Card from "primevue/card";
import Button from "primevue/button";
import Dialog from "primevue/dialog";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import { ref } from "vue";

const visible = ref(false);

const files = ref([
  { file_name: "File 1" },
  { file_name: "File 2" },
  { file_name: "File 3" },
]);
</script>
<template>
  <Card>
    <template #title>
      <div class="flex justify-between item-center">
        <p>Knowledge Pulse</p>
        <Button label="Manage DB" @click="visible = true" />
      </div>
    </template>
  </Card>
  <Dialog
    v-model:visible="visible"
    maximizable
    modal
    header="Files"
    :style="{ width: '50rem' }"
    :breakpoints="{ '1199px': '75vw', '575px': '90vw' }"
  >
    <div class="flex justify-end">
      <Button
        label="Upload new files"
        severity="secondary"
        icon="pi pi-plus"
        iconPos="left"
      />
    </div>
    <div>
      <DataTable :value="files" :size="'small'">
        <Column field="file_name" header="File Name"></Column>
      </DataTable>
    </div>
  </Dialog>
</template>

<script setup lang="ts">
import Card from "primevue/card";
import Button from "primevue/button";
import Dialog from "primevue/dialog";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import FileUpload from "primevue/fileupload";
import { ref } from "vue";

const visible = ref(false);

const files = ref([]);

const uploadUrl = import.meta.env.VITE_API_URL + "/files/upload";
const fileListUrl = import.meta.env.VITE_API_URL + "/files/list";

const fileList = async () => {
  try {
    const response = await fetch(fileListUrl);
    const response_data = await response.json();
    files.value = response_data;
  } catch (e) {
    console.error(e);
  }
};
fileList();
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
      <FileUpload
        mode="basic"
        name="files"
        :url="uploadUrl"
        accept=".pdf,.docx,.doc,.txt"
        :maxFileSize="10000000"
        :auto="true"
        :multiple="true"
        @click="fileList()"
        chooseLabel="Upload File"
      />
    </div>
    <div>
      <DataTable :value="files" :size="'small'">
        <Column field="file_name" header="File Name"></Column>
      </DataTable>
    </div>
  </Dialog>
</template>

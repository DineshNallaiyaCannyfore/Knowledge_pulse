<script setup lang="ts">
import Card from "primevue/card";
import Button from "primevue/button";
import Dialog from "primevue/dialog";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import FileUpload from "primevue/fileupload";
import { onMounted, ref, watch } from "vue";
import { useStore } from "../stores/store";

const visible = ref(false);
const uploading = ref(false);
const store = useStore();
const files = ref([]);

const uploadUrl = import.meta.env.VITE_API_URL + "/files/upload";

onMounted(() => {
  store.fetchFileList();
});

watch(
  () => store.fileList,
  (newFileList) => {
    files.value = newFileList;
  },
  { immediate: true },
);

const onBeforeUpload = () => {
  uploading.value = true;
};

const onAfterUpload = () => {
  uploading.value = false;
  store.fetchFileList();
};
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
        chooseLabel="Upload File"
        @upload="onAfterUpload"
        @before-upload="onBeforeUpload"
        :disabled="uploading"
      />
    </div>
    <div
      v-if="uploading"
      class="text-sm text-gray-500 p-2 m-2 flex items-center justify-center"
    >
      <i class="pi pi-spin pi-spinner" style="font-size: 16px"></i>&nbsp;&nbsp;
      Uploading...
    </div>
    <div>
      <DataTable :value="files" :size="'small'" :loading="store.isLoading">
        <template #empty>
          <div class="text-center text-gray-500 text-[12px]">
            No files found...
          </div>
        </template>
        <Column field="file_name" header="File Name"></Column>
      </DataTable>
    </div>
  </Dialog>
</template>

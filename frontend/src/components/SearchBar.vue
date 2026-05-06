<script setup lang="ts">
import { ref } from "vue";
import Card from "primevue/card";
import InputText from "primevue/inputtext";
import Button from "primevue/button";
import Skeleton from "primevue/skeleton";
import { useToast } from "primevue/usetoast";
import Toast from "primevue/toast";
const toast = useToast();

interface SearchResult {
  request?: string;
  llm_answer?: string;
  source_document?: string[];
}
const searchUrl = import.meta.env.VITE_API_URL + "/search/find";

const searchQuery = ref("");
const isLoading = ref(false);
const searchResults = ref<SearchResult[]>([]);

const displayToast = (severity: string, summary: string, detail: string) => {
  toast.add({
    severity,
    summary,
    detail,
    life: 3000,
  });
};

const performSearch = async () => {
  isLoading.value = true;
  if (!searchQuery.value.trim()) {
    isLoading.value = false;
    displayToast("warn", "Warning", "Please enter a search query.");
    return;
  }
  try {
    searchResults.value.push({ request: searchQuery.value });
    const response = await fetch(searchUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query: searchQuery.value }),
    });
    const data = await response.json();
    searchResults.value.push(data);
    searchQuery.value = "";
  } catch (e) {
    console.error("Search error:", e);
    searchResults.value.pop();
    displayToast("error", "Error", "Something went wrong. Please try again.");
  } finally {
    isLoading.value = false;
  }
};

const handleKeyPress = (event: KeyboardEvent) => {
  if (event.key === "Enter") {
    if (searchQuery.value.trim()) {
      performSearch();
    } else {
      displayToast("warn", "Warning", "Please enter a search query.");
    }
  }
};
</script>

<style scoped>
:deep(.p-card-body) {
  padding: 7px !important;
  font-size: 14px;
}
</style>

<template>
  <div class="h-[calc(100vh-100px)] flex flex-col overflow-hidden">
    <div class="flex-1 overflow-y-auto p-4 pb-5">
      <div class="flex justify-center">
        <div class="w-[80%]">
          <div
            v-for="(result, index) in searchResults"
            :key="index"
            :class="[
              'flex my-3',
              result.request ? 'justify-end' : 'justify-start',
            ]"
          >
            <Card
              :class="[
                'w-fit max-w-[70%]',
                result.request ? 'bg-blue-100' : 'bg-gray-100',
              ]"
            >
              <template #content>
                <p>
                  {{ result?.request || result?.llm_answer }}
                </p>
                <small
                  v-if="
                    Array.isArray(result.source_document) &&
                    result.source_document.length
                  "
                  class="ml-2 mt-1 text-gray-500"
                >
                  Source: {{ result.source_document.join(", ") }}
                </small>
              </template>
            </Card>
          </div>
          <div v-if="isLoading">
            <Skeleton height="70px" width="700px" class="mb-2"></Skeleton>
          </div>
        </div>
      </div>
    </div>

    <div class="p-4 flex justify-center">
      <InputText
        v-model="searchQuery"
        placeholder="Ask me anything..."
        @keypress="handleKeyPress"
        class="w-[50%]"
      />
      <Button icon="pi pi-search" @click="performSearch" rounded class="ml-2" />
      <div class="card flex justify-center">
        <Toast />
      </div>
    </div>
  </div>
</template>

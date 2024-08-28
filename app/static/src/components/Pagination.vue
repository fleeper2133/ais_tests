<template>
    <div class="pagination">
        <button class="word-button" :disabled="currentPage === 1" :style="`opacity: ${currentPage === 1 ? '0.5' : '1'};`" @click="prevPage">Предыдущая</button>
        
        <button
            class="pagination-button"
            v-for="page in visiblePages"
            :key="page"
            :class="{ active: currentPage === page }"
            @click="goToPage(page)"
        >
            {{ page }}
        </button>
    
        <button class="word-button" :disabled="currentPage === totalPages" :style="`opacity: ${currentPage === totalPages ? '0.5' : '1'};`" @click="nextPage">Следующая</button>
    </div>
</template>
  
<script setup lang="ts">
import { ref, computed } from 'vue';

const props = defineProps({
  currentPage: {
    type: Number,
    required: true,
  },
  itemsPerPage: {
    type: Number,
    required: true,
  },
  totalItems: {
    type: Number,
    required: true,
  },
});

const emit = defineEmits(['update:currentPage']);

const visiblePagesCount = 5;

const totalPages = computed(() =>
  Math.ceil(props.totalItems / props.itemsPerPage)
);

const visiblePages = computed(() => {
  const halfVisiblePagesCount = Math.floor(visiblePagesCount / 2);
  let startPage = props.currentPage - halfVisiblePagesCount;
  let endPage = props.currentPage + halfVisiblePagesCount;
  if (startPage < 1) {
    endPage -= startPage - 1;
    startPage = 1;
  }

  if (endPage > totalPages.value) {
    startPage -= endPage - totalPages.value;
    endPage = totalPages.value;
  }
  if( startPage < 1) startPage = 1
    const pages = [];
    for (let i = startPage; i <= endPage; i++) {
        pages.push(i);
  }

  return pages;
});

const prevPage = () => {
  if (props.currentPage > 1) {
    emit('update:currentPage', props.currentPage - 1);
  }
};

const nextPage = () => {
  if (props.currentPage < totalPages.value) {
    emit('update:currentPage', props.currentPage + 1);
  }
};

const goToPage = (page: number) => {
  emit('update:currentPage', page);
};

</script>

<style lang="scss" scoped>

@import '../sass/main.scss';

.pagination {
    margin: 0 auto;
    display: flex;
    gap: 10px;
}

.pagination-button {
    cursor: pointer;
    width: 40px;
    height: 40px;
}
.active {
    color: $main-blue;
    border: 1px solid $border;
}
.word-button {
    cursor: pointer;
}

@media (max-width: 768px) {
    .pagination-button {
        width: 30px;
        height: 30px;
        font-size: 14px;
    }

    .word-button {
        font-size: 14px;
    }
}

@media (max-width: 480px) {
    .pagination-button {
        width: 25px;
        height: 25px;
        font-size: 12px;
    }

    .word-button {
        font-size: 12px;
    }
}
</style>


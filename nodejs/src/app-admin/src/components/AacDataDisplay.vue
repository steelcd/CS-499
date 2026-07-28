<template>
  <div class="animals-page">
    <h2>AAC Data</h2>

    <div v-if="loading" class="loading">
      Loading items, please wait...
    </div>

    <div v-else-if="error" class="error-msg">
      Error loading data: {{ error }}
    </div>

    <div v-else-if="items.length === 0" class="empty-msg">
    No animals found.
    </div>

    <div v-else class="scroll-panel">
      <table>

        <thead>
          <tr>
            <th>Shelter</th>
            <th>Animal ID</th>
            <th>Name</th>
            <th>Type</th>
            <th>Breed</th>
            <th>Color</th>
            <th>Sex</th>
            <th>DOB</th>
            <th>Actions</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="animal in items" :key="animal._id || animal.animal_id">
            <td class="nowrap">{{ animal.shelter }}</td>
            <td>{{ animal.animal_id }}</td>
            <td>{{ animal.name || 'Unnamed' }}</td>
            <td>{{ animal.animal_type }}</td>
            <td>{{ animal.breed }}</td>
            <td>{{ animal.color }}</td>
            <td>{{ animal.sex_upon_outcome }}</td>
            <td>{{ formatDate(animal.date_of_birth) }}</td>
            <td class="actions-cell">
              <RouterLink
                class="action-link"
                :to="`/animals/${animal.animal_id}/edit`"
              >
                Edit
              </RouterLink>

              <button
                type="button"
                class="action-button danger"
                @click="deleteAnimal(animal.animal_id)"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// Define reactive state variables
const items = ref([])
const loading = ref(true)
const error = ref(null)

// Date format function
const formatDate = (value) => {
  if (!value) return ''

  return new Date(value).toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

// Define the asynchronous data fetching function
const fetchData = async () => {
  try {
    const response = await fetch('/api/admin/animals')
    
    // Check if the server response is successful (status 200-299)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    // Parse the response body as JSON and update the reactive array
    items.value = await response.json()
  } catch (err) {
    // Catch and record network or parsing errors
    error.value = err.message
  } finally {
    // Always hide the loading state when done
    loading.value = false
  }
}

// Trigger the API request immediately after the component mounts to the DOM
onMounted(() => {
  fetchData()
})

async function deleteAnimal(animalId) {
  const confirmed = window.confirm(`Delete animal ${animalId}?`)

  if (!confirmed) {
    return
  }

  const response = await fetch(`/api/admin/animals/${animalId}`, {
    method: 'DELETE',
  })

  if (!response.ok) {
    throw new Error(`Failed to delete animal ${animalId}`)
  }

  items.value = items.value.filter((animal) => animal.animal_id !== animalId)
}
</script>

<style scoped>
  .animals-page {
    height: 100vh;
    padding: 24px;
    display: flex;
    flex-direction: column;
    min-width: 0;
  }

  .animals-page h2 {
    margin: 0 0 16px;
    color: #243447;
  }

  .loading,
  .empty-msg {
    color: #52616f;
  }

  .error-msg {
    color: #b42318;
    font-weight: 700;
  }

  .scroll-panel {
    flex: 1;
    overflow: auto;
    min-height: 0;
    border: 1px solid #d9e2ec;
  }

  .nowrap {
  white-space: nowrap;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    table-layout: auto;
    background: #ffffff;
  }

  thead {
    position: sticky;
    top: 0;
    z-index: 1;
    background: #f4f7fa;
  }

  th,
  td {
    padding: 10px 12px;
    border-bottom: 1px solid #e6edf3;
    text-align: left;
    vertical-align: top;
    color: #243447;
  }

  th {
    font-size: 0.8rem;
    font-weight: 700;
    color: #52616f;
    text-transform: uppercase;
  }

  td {
    font-size: 0.95rem;
  }

  tbody tr:nth-child(even) {
    background: #f8fafc;
  }

  tbody tr:hover {
    background: #eef6f3;
  }

  .actions-cell {
    white-space: nowrap;
  }

  .action-link,
  .action-button {
    margin-right: 8px;
    font: inherit;
    color: #2f6f5e;
    background: none;
    border: 0;
    cursor: pointer;
    text-decoration: underline;
  }

  .action-button.danger {
  color: #b42318;
  }
</style>

<template>
  <form class="animal-form" @submit.prevent="handleSubmit">
    <div class="form-grid">
      <label>
        Animal ID
        <input v-model="form.animal_id" type="text" required>
      </label>

      <label>
        Name
        <input v-model="form.name" type="text">
      </label>

      <label>
        Type
        <input v-model="form.animal_type" type="text" required>
      </label>

      <label>
        Breed
        <input v-model="form.breed" type="text" required>
      </label>

      <label>
        Color
        <input v-model="form.color" type="text" required>
      </label>

      <label>
        Date of Birth
        <input v-model="form.date_of_birth" type="date" required>
      </label>

      <label>
        Sex
        <input v-model="form.sex_upon_outcome" type="text" required>
      </label>

      <label>
        Outcome Type
        <input v-model="form.outcome_type" type="text" required>
      </label>

      <label>
        Outcome Subtype
        <input v-model="form.outcome_subtype" type="text">
      </label>

      <label>
        Age Upon Outcome
        <input v-model="form.age_upon_outcome" type="text" required>
      </label>

      <label>
        Age in Weeks
        <input v-model="form.age_upon_outcome_in_weeks" type="number" step="any" required>
      </label>

      <label>
        Latitude
        <input v-model="form.location_lat" type="number" step="any" required>
      </label>

      <label>
        Longitude
        <input v-model="form.location_long" type="number" step="any" required>
      </label>

      <label>
        Shelter
        <input v-model="form.shelter" type="text" required>
      </label>
    </div>

    <div class="form-actions">
      <button type="submit">{{ submitLabel }}</button>
      <button type="button" @click="emit('cancel')">Cancel</button>
    </div>
  </form>
</template>

<script setup>
import { reactive, watch } from 'vue'

const props = defineProps({
  initialAnimal: {
    type: Object,
    default: () => ({}),
  },
  submitLabel: {
    type: String,
    default: 'Save Animal',
  },
})

const emit = defineEmits(['submit', 'cancel'])

const form = reactive({
  animal_id: '',
  name: '',
  animal_type: '',
  breed: '',
  color: '',
  date_of_birth: '',
  sex_upon_outcome: '',
  outcome_type: '',
  outcome_subtype: '',
  age_upon_outcome: '',
  age_upon_outcome_in_weeks: '',
  location_lat: '',
  location_long: '',
  shelter: '',
})

watch(
  () => props.initialAnimal,
  (animal) => {
    Object.assign(form, {
      animal_id: animal.animal_id || '',
      name: animal.name || '',
      animal_type: animal.animal_type || '',
      breed: animal.breed || '',
      color: animal.color || '',
      date_of_birth: formatDateForInput(animal.date_of_birth),
      sex_upon_outcome: animal.sex_upon_outcome || '',
      outcome_type: animal.outcome_type || '',
      outcome_subtype: animal.outcome_subtype || '',
      age_upon_outcome: animal.age_upon_outcome || '',
      age_upon_outcome_in_weeks: animal.age_upon_outcome_in_weeks || '',
      location_lat: animal.location_lat || '',
      location_long: animal.location_long || '',
      shelter: animal.shelter || '',
    })
  },
  { immediate: true }
)

function formatDateForInput(value) {
  if (!value) return ''

  return new Date(value).toISOString().slice(0, 10)
}

function handleSubmit() {
  emit('submit', {
    ...form,
    age_upon_outcome_in_weeks: Number(form.age_upon_outcome_in_weeks),
    location_lat: Number(form.location_lat),
    location_long: Number(form.location_long),
  })
}
</script>

<style scoped>
.animal-form {
  max-width: 960px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(220px, 1fr));
  gap: 16px;
}

label {
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-weight: 700;
  color: #52616f;
}

input {
  padding: 9px 10px;
  border: 1px solid #cbd5df;
  font: inherit;
  color: #243447;
  background: #ffffff;
}

input:focus {
  outline: 2px solid #a7d7c5;
  border-color: #3a7d6b;
}

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 20px;
}

button {
  padding: 9px 14px;
  border: 1px solid #3a7d6b;
  background: #3a7d6b;
  color: #ffffff;
  font-weight: 700;
  cursor: pointer;
}

button[type="button"] {
  background: #ffffff;
  color: #3a7d6b;
}

@media (max-width: 700px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
}
</style>
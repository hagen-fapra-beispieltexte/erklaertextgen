<template>
  <div>
    <Teacher @goToStudentView="goToStudentView" />
  </div>
</template>

<script>
import Teacher from '../components/TeacherComponent.vue'

export default {
  components: {
    Teacher
  },
  methods: {
    goToStudentView() {
      this.$router.push('/');
    }
  }
}
</script>

<style>
/* Add your styles here */
</style>
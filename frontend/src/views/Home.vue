<template>
  <div class="home"></div>
</template>

<script>
export default {
  name: "Home",
  components: {},
  mounted() {
    this.$router.push({ name: "PreSession" });
  },
};
</script>

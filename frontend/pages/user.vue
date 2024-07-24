<template>
    <div class="user-container">
      <h1>Your User Info</h1>
      <table v-if="user">
        <tr>
          <th>ID</th>
          <td>{{ user.id }}</td>
        </tr>
        <tr>
          <th>Username</th>
          <td>{{ user.username }}</td>
        </tr>
        <tr>
          <th>Staff</th>
          <td>{{ user.is_staff ? 'Yes' : 'No'  }}</td>
        </tr>
        <tr>
          <th>Active</th>
          <td>{{ user.is_active ? 'Yes' : 'No' }}</td>
        </tr>
      </table>
      <div v-else>
        <p>Loading user info...</p>
      </div>
    </div>
  </template>

<script>
export default {
  data() {
    return {
      user: null
    };
  },
  created() {
    this.fetchUser();
  },
  methods: {
    async fetchUser() {
      const jwt_token = localStorage.getItem('jwt_token');

      if (!jwt_token) {
        console.error('No JWT token found');
        return;
      }

      try {
        // API 只會返回單個 User
        const response = await this.$axios.get(
          '/user/info',
          {
            headers: { 'Authorization': `Bearer ${jwt_token}` }
          }
        );
        this.user = response.data;
      } catch (error) {
        console.error('Error fetching user:', error);
      }
    }
  }
}
</script>

<style scoped>
.user-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  border-radius: 8px;
  background-color: #f9f9f9;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  color: #333;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #f2f2f2;
  color: #333;
}

td {
  color: #555;
}

tr:hover {
  background-color: #f1f1f1;
}
</style>
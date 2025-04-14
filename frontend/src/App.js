// =======================
// 📦 FRONTEND (App.js)
// =======================
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Box, AppBar, Toolbar, Typography, TextField, Container, Pagination } from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';

function App() {
  const [transactions, setTransactions] = useState([]);
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const pageSize = 10;

  const fetchTransactions = () => {
    axios
      .get(`http://localhost:8000/transactions?search=${search}&page=${page}&limit=${pageSize}`)
      .then((res) => {
        setTransactions(res.data.transactions);
        setTotalPages(res.data.total_pages);
      });
  };

  useEffect(() => {
    fetchTransactions();
  }, [search, page]);

  const columns = [
    { field: 'transaction_id', headerName: 'ID', width: 250 },
    { field: 'from_user', headerName: 'User', width: 150 },
    { field: 'to_merchant', headerName: 'Merchant', width: 200 },
    { field: 'amount', headerName: 'Amount', width: 100 },
  ];

  return (
    <Box>
      <AppBar position="fixed">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>Live Transactions</Typography>
        </Toolbar>
      </AppBar>
      <Toolbar />
      <Container sx={{ mt: 4 }}>
        <TextField
          label="Search by ID, User, Merchant"
          variant="outlined"
          fullWidth
          value={search}
          onChange={(e) => {
            setSearch(e.target.value);
            setPage(1);
          }}
        />

        <Box sx={{ mt: 2, height: 500 }}>
          <DataGrid
            rows={transactions}
            columns={columns}
            getRowId={(row) => row.transaction_id}
            rowHeight={40}
            disableRowSelectionOnClick
            pagination={false}
          />
        </Box>

        <Box display="flex" justifyContent="center" mt={2}>
          <Pagination count={totalPages} page={page} onChange={(e, value) => setPage(value)} />
        </Box>
      </Container>
    </Box>
  );
}

export default App;

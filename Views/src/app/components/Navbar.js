"use client";

// app/components/Navbar.js
import React from 'react';
import { AppBar, Toolbar, Typography, IconButton, Button, Drawer, List, ListItem, ListItemText } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function Navbar() {
  const [drawerOpen, setDrawerOpen] = useState(false);
  const router = useRouter();

  const handleDrawerToggle = () => {
    setDrawerOpen(!drawerOpen);
  };

  const handleNavLink = (path) => {
    router.push(path);
    setDrawerOpen(false);  // Close drawer on navigation
  };

  const navItems = [
    { text: 'Home', path: '/' },
    { text: 'About', path: '/about' },
    { text: 'Contact', path: '/contact' },
    { text: 'Login', path: '/login' },
  ];

  return (
    <AppBar position="static">
      <Toolbar>
        {/* 漢堡菜單按鈕（小螢幕顯示） */}
        <IconButton
          edge="start"
          color="inherit"
          aria-label="menu"
          onClick={handleDrawerToggle}
          sx={{ display: { xs: 'block', sm: 'none' } }}
        >
          <MenuIcon />
        </IconButton>

        {/* 標題 */}
        <Typography variant="h6" sx={{ flexGrow: 1 }}>
          My Website
        </Typography>

        {/* 導航按鈕（大螢幕顯示） */}
        <div sx={{ display: { xs: 'none', sm: 'block' } }}>
          {navItems.map((item) => (
            <Button key={item.text} color="inherit" onClick={() => handleNavLink(item.path)}>
              {item.text}
            </Button>
          ))}
        </div>
      </Toolbar>

      {/* 抽屜菜單（小螢幕顯示） */}
      <Drawer anchor="left" open={drawerOpen} onClose={handleDrawerToggle}>
        <List>
          {navItems.map((item) => (
            <ListItem button key={item.text} onClick={() => handleNavLink(item.path)}>
              <ListItemText primary={item.text} />
            </ListItem>
          ))}
        </List>
      </Drawer>
    </AppBar>
  );
}

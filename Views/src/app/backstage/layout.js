import React from 'react';
import styles from '../backstage.module.css';

export default function BackstageLayout({ children }) {
  return (
    <div className={styles.backstage}>
      {children}
    </div>
  );
}
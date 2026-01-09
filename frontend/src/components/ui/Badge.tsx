import React from 'react';
import styles from './Badge.module.css';

type BadgeType = 'full-time' | 'part-time' | 'internship' | 'contract' | 'temporary';

interface BadgeProps {
  type: BadgeType;
  className?: string;
}

const badgeTypeMap: Record<BadgeType, string> = {
  'full-time': 'fulltime',
  'part-time': 'parttime',
  'internship': 'internship',
  'contract': 'contract',
  'temporary': 'temporary',
};

const labels: Record<BadgeType, string> = {
  'full-time': 'Full-Time',
  'part-time': 'Part-Time',
  'internship': 'Internship',
  'contract': 'Contract',
  'temporary': 'Temporary',
};

export const Badge: React.FC<BadgeProps> = ({ type, className = '' }) => {
  return (
    <span className={`${styles.badge} ${styles[badgeTypeMap[type]]} ${className}`}>
      {labels[type]}
    </span>
  );
};

import React from 'react';
import { Box } from '@chakra-ui/react';

const TerminalWindow = ({ children }) => {
  return (
    <Box
      border="1px solid"
      borderColor="gray.700"
      borderRadius="md"
      bg="gray.900"
      p={6}
      width="100%"
      maxWidth="800px"
      boxShadow="lg"
    >
      {children}
    </Box>
  );
};

export default TerminalWindow;

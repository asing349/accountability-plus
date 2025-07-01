import React from 'react';
import { Box, Text, Link, Flex, Image } from '@chakra-ui/react';

const Footer = () => {
  const githubLink = "https://github.com/asing349?tab=repositories";
  const linkedinLink = "https://www.linkedin.com/in/itsmejait";
  const githubLogo = "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png";
  const linkedinLogo = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/LinkedIn_logo_initials.png/640px-LinkedIn_logo_initials.png";

  return (
    <Box
      as="footer"
      width="100%"
      py={4}
      bg="gray.900"
      borderTop="1px solid"
      borderColor="gray.700"
      textAlign="center"
      fontFamily="monospace"
      color="gray.500"
      fontSize="sm"
    >
      <Flex justify="center" align="center" mb={2}>
        <Link href={githubLink} isExternal mx={2}>
          <Image src={githubLogo} alt="GitHub" boxSize="24px" />
        </Link>
        <Link href={linkedinLink} isExternal mx={2}>
          <Image src={linkedinLogo} alt="LinkedIn" boxSize="24px" />
        </Link>
      </Flex>
      <Text mb={1}>Warning: Only for test. Does not guarantee validity of the data as it is a project.</Text>
      <Text>&copy; {new Date().getFullYear()} Accountability++</Text>
    </Box>
  );
};

export default Footer;

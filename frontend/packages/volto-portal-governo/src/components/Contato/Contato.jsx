import React from 'react';
import PropTypes from 'prop-types';
import { Container } from '@plone/components';

const Contato = (props) => {
  const { telefone, email } = props.content;

  return (
    <Container narrow className="contato">
      <Container className="telefone">
        <span>Telefone</span>: <span>{telefone}</span>
      </Container>
      <Container className="email">
        <span>E-mail</span>: <a href={`mailto:${email}`}>{email}</a>
      </Container>
    </Container>
  );
};

Contato.propTypes = {
  content: PropTypes.shape({
    email: PropTypes.string,
    telefone: PropTypes.string,
  }).isRequired,
};

export default Contato;

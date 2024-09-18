import React from 'react';
import PropTypes from 'prop-types';
import { getBaseUrl } from '@plone/volto/helpers';
import { Container } from '@plone/components';
import Contato from '../Contato/Contato';
import Endereco from '../Endereco/Endereco';
import Gestor from '../Gestor/Gestor';
import RenderBlocks from '@plone/volto/components/theme/View/RenderBlocks';

const SecretariaView = (props) => {
  const { content, location } = props;
  const { endereco, complemento, cidade, estado, cep } = content;
  const path = getBaseUrl(location?.pathname || '');

  return (
    <Container id="page-document" className="view-wrapper secretaria-view">
      <RenderBlocks {...props} path={path} />
      <Endereco content={content} />
      <Contato content={content} />
      <Gestor content={content.gestor} />
    </Container>
  );
};

/**
 * Property types.
 * @property {Object} propTypes Property types.
 * @static
 */
SecretariaView.propTypes = {
  content: PropTypes.shape({
    title: PropTypes.string,
    description: PropTypes.string,
    email: PropTypes.string,
    telefone: PropTypes.string,
  }).isRequired,
};

export default SecretariaView;
